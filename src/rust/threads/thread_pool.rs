use std::sync::{Arc, mpsc, Mutex};
use std::thread;

type Job = Box<dyn FnOnce() + Send + 'static>;

enum Message {
    NewJob(Job),
    Terminate,
}

pub struct ThreadPool {
    workers: Vec<Worker>,
    sender: mpsc::Sender<Message>,
}

impl ThreadPool {
    /// Create a new ThreadPool.
    ///
    /// The size is the number of workers in the pool.
    ///
    /// # Panics
    ///
    /// The `new` function will panic if the size is zero.
    pub fn new(size: usize) -> ThreadPool {
        assert!(size > 0);
        let (sender, receiver) = mpsc::channel();
        let receiver = Arc::new(Mutex::new(receiver));

        let mut workers = Vec::with_capacity(size);

        for id in 0..size {
            workers.push(Worker::new(id, Arc::clone(&receiver)));
        }

        ThreadPool {
            workers,
            sender
        }
    }

    pub fn execute<F>(&self, f: F)
        where
            F: FnOnce() + Send + 'static {

        let job = Box::new(f);
        self.sender.send(Message::NewJob(job)).unwrap();
    }
}

impl Drop for ThreadPool {
    fn drop(&mut self) {
        println!("Sending terminate message to all workers.");
        // Attention

        // "To better understand why we need two separate loops, imagine a scenario with two
        // workers. If we used a single loop to iterate through each worker, on the first
        // iteration a terminate message would be sent down the channel and join called on
        // the first worker’s thread. If that first worker was busy processing a request at
        // that moment, the second worker would pick up the terminate message from the
        // channel and shut down. We would be left waiting on the first worker to shut down,
        // but it never would because the second thread picked up the terminate message.
        // Deadlock!

        // To prevent this scenario, we first put all of our Terminate messages on the
        // channel in one loop; then we join on all the threads in another loop. Each worker
        // will stop receiving requests on the channel once it gets a terminate message. So,
        // we can be sure that if we send the same number of terminate messages as there are
        // workers, each worker will receive a terminate message

        for _ in &mut self.workers {
            self.sender.send(Message::Terminate).unwrap();
        }

        for worker in &mut self.workers {
            println!("Shutting down worker {}", worker.id);

            if let Some(thread) = worker.thread.take() {
                thread.join().unwrap();
            }
        }
    }
}


struct Worker {
    id: usize,
    thread: Option<thread::JoinHandle<()>>,
}

impl Worker {
    fn new(id: usize, receiver: Arc<Mutex<mpsc::Receiver<Message>>>) -> Worker {
        let thread = thread::spawn(move || {
            loop {
                let message = receiver
                    .lock()
                    .expect("Lock in poisoned state, prior acquirer panicked")
                    .recv()
                    .unwrap();

                match message {
                    Message::NewJob(job) => {
//                        println!("Worker {} got a job; executing.", id);
                        job();
                    },
                    Message::Terminate => {
//                        println!("Worker {} was told to terminate.", id);
                        break;
                    },
                }
            }
        });

        Worker {
            id,
            thread: Some(thread),
        }
    }
}