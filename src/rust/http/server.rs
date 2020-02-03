use std::error;
use std::fs;
use std::io::prelude::*;
use std::net::{TcpListener, TcpStream};

use rust::threads::thread_pool::ThreadPool;

const PORT_SEP: &str = ":";
const PATH_SEP: &str = "/";
const OK_STATUS_LN: &str = "HTTP/1.1 200 OK\r\n\r\n";
const NYI_STATUS_LN: &str = "HTTP/1.1 501 NOT IMPLEMENTED\r\n\r\n";
const NOT_FOUND_STATUS_LN: &str = "HTTP/1.1 404 NOT FOUND\r\n\r\n";
const EMPTY_CONTENTS: &str = "";

const NOT_FOUND_PATH: &str = "serve/404.html";

#[derive(Debug)]
enum HttpStatus {
    Ok,
    NotFound,
    NotImplemented
}

pub struct HttpServer {
    num_threads: usize
}

fn handle_connection(mut stream: TcpStream) {
    let mut buffer = [0; 512];

    stream.read(&mut buffer).unwrap();

    let text = &String::from_utf8_lossy(&buffer[..]);
    let mut tokens = text.split_whitespace();
    let verb = tokens.next().unwrap();
    let path = tokens.next().unwrap();

    let (status, file_path) = if verb == "GET" && path == "/" {
        (HttpStatus::Ok, "serve/chess.html".to_owned())
    } else if verb != "GET" {
        (HttpStatus::NotImplemented, "serve/501.html".to_owned())
    } else {
        let path_tokens: Vec<_> = path.split(PATH_SEP).collect();

        if path_tokens.len() < 3 || path_tokens.len() > 4 {
            (HttpStatus::NotFound, NOT_FOUND_PATH.to_owned())
        } else {
            let mut vec = Vec::new();
            vec.push("serve");
            vec.push(path_tokens[2]);

            if path_tokens.len() == 4 {
                vec.push(path_tokens[3]);
            }
            let last_token = if  path_tokens.len() == 4 { path_tokens[3] } else { "" };
            (HttpStatus::Ok, vec.join(PATH_SEP))
        }
    };

    let response = match status {
        HttpStatus::Ok => {
            let (status_ln, contents) = fs::read_to_string(file_path)
                .map(|c| (OK_STATUS_LN, c))
                .or(fs::read_to_string(NOT_FOUND_PATH).map(|c| (OK_STATUS_LN, c)))
                .unwrap_or((NOT_FOUND_STATUS_LN, EMPTY_CONTENTS.to_owned()));

            format!("{}{}", status_ln, contents)
        },
        HttpStatus::NotImplemented => NYI_STATUS_LN.to_owned(),
        HttpStatus::NotFound => NOT_FOUND_STATUS_LN.to_owned(),
    };

    stream.write(response.as_bytes()).unwrap();
    stream.flush().unwrap();
}

impl HttpServer {
    pub fn new(num_threads: usize) -> HttpServer {
        HttpServer {
            num_threads
        }
    }

    pub fn bind(&self, host: &str, port: u32) -> Result<(), Box<dyn error::Error>> {
        let addr_str = [host, PORT_SEP, &port.to_string()].concat();
        let listener = TcpListener::bind(addr_str)?;
        let thread_pool = ThreadPool::new(self.num_threads);

        for stream in listener.incoming() {
            let stream = stream.unwrap();

            thread_pool.execute(|| {
                handle_connection(stream);
            });
        }
        Ok(())
    }
}

