use std::error;

mod rust;

fn main() -> Result<(), Box<dyn error::Error>> {
    use rust::http::server::HttpServer;
    let server = HttpServer::new(4);
    server.bind("127.0.0.1", 5000)?;
    Ok(())
}