use std::error;
use rust::http::server::{HttpRequest, HttpResponse};

mod rust;

fn main() -> Result<(), Box<dyn error::Error>> {
    use rust::http::server::HttpServer;
    use rust::http::router::route;
    let server = HttpServer::new(4);
    server.bind("127.0.0.1", 5000, &(route as fn(HttpRequest) -> HttpResponse))?;
    Ok(())
}