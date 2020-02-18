use std::{error, io};
use std::io::prelude::*;
use std::io::Read;
use std::net::{TcpListener, TcpStream};

use rust::threads::thread_pool::ThreadPool;

const PORT_SEP: &str = ":";
const HTTP_1_1: &str = "HTTP/1.1";
const HTTP_LINE_BREAK: &str = "\r\n\r\n";
const CARRIAGE_RETURN: u8 = 13;
const LINE_FEED: u8 = 10;

// https://tools.ietf.org/html/rfc7231#section-6.5.1
#[derive(Debug)]
pub enum HttpStatusCode {
    Continue                    = 100,
    SwitchingProtocols          = 101,
    Ok                          = 200,
    Created                     = 201,
    Accepted                    = 202,
    NonAuthoritativeInformation = 203,
    NoContent                   = 204,
    ResetContent                = 205,
    PartialContent              = 206,
    MultipleChoices             = 300,
    MovedPermanently            = 301,
    Found                       = 302,
    SeeOther                    = 303,
    NotModified                 = 304,
    UseProxy                    = 305,
    TemporaryRedirect           = 307,
    BadRequest                  = 400,
    Unauthorized                = 401,
    PaymentRequired             = 402,
    Forbidden                   = 403,
    NotFound                    = 404,
    MethodNotAllowed            = 405,
    NotAcceptable               = 406,
    ProxyAuthenticationRequired = 407,
    RequestTimeout              = 408,
    Conflict                    = 409,
    Gone                        = 410,
    LengthRequired              = 411,
    PreconditionFailed          = 412,
    PayloadTooLarge             = 413,
    UriTooLong                  = 414,
    UnsupportedMediaType        = 415,
    RangeNotSatisfiable         = 416,
    ExpectationFailed           = 417,
    UpgradeRequired             = 426,
    InternalServerError         = 500,
    NotImplemented              = 501,
    BadGateway                  = 502,
    ServiceUnavailable          = 503,
    GatewayTimeout              = 504,
    HttpVersionNotSupported     = 505
}

#[derive(Debug)]
pub struct HttpStatus {
    code: HttpStatusCode,
    reason: &'static str
}

pub fn code_to_status(status: &HttpStatusCode) -> HttpStatus {
    match status {
        HttpStatusCode::Continue                    =>
            HttpStatus{ code: HttpStatusCode::Continue, reason: "CONTINUE" },
        HttpStatusCode::SwitchingProtocols          =>
            HttpStatus{ code: HttpStatusCode::SwitchingProtocols, reason: "SWITCHING PROTOCOLS" },
        HttpStatusCode::Ok                          =>
            HttpStatus{ code: HttpStatusCode::Ok, reason: "OK" },
        HttpStatusCode::Created                     =>
            HttpStatus{ code: HttpStatusCode::Created, reason: "CREATED" },
        HttpStatusCode::Accepted                    =>
            HttpStatus{ code: HttpStatusCode::Accepted, reason: "ACCEPTED" },
        HttpStatusCode::NonAuthoritativeInformation =>
            HttpStatus{ code: HttpStatusCode::NonAuthoritativeInformation, reason: "NON-AUTHORITATIVE INFORMATION" },
        HttpStatusCode::NoContent                   =>
            HttpStatus{ code: HttpStatusCode::NoContent, reason: "NO CONTENT" },
        HttpStatusCode::ResetContent                =>
            HttpStatus{ code: HttpStatusCode::ResetContent, reason: "RESET CONTENT" },
        HttpStatusCode::PartialContent              =>
            HttpStatus{ code: HttpStatusCode::PartialContent, reason: "PARTIAL CONTENT" },
        HttpStatusCode::MultipleChoices             =>
            HttpStatus{ code: HttpStatusCode::MultipleChoices, reason: "MULTIPLE CHOICES" },
        HttpStatusCode::MovedPermanently            =>
            HttpStatus{ code: HttpStatusCode::MovedPermanently, reason: "MOVED PERMANENTLY" },
        HttpStatusCode::Found                       =>
            HttpStatus{ code: HttpStatusCode::Found, reason: "FOUND" },
        HttpStatusCode::SeeOther                    =>
            HttpStatus{ code: HttpStatusCode::SeeOther, reason: "SEE OTHER" },
        HttpStatusCode::NotModified                 =>
            HttpStatus{ code: HttpStatusCode::NotModified, reason: "NOT MODIFIED" },
        HttpStatusCode::UseProxy                    =>
            HttpStatus{ code: HttpStatusCode::UseProxy, reason: "USE PROXY" },
        HttpStatusCode::TemporaryRedirect           =>
            HttpStatus{ code: HttpStatusCode::TemporaryRedirect, reason: "TEMPORARY REDIRECT" },
        HttpStatusCode::BadRequest                  =>
            HttpStatus{ code: HttpStatusCode::BadRequest, reason: "BAD REQUEST" },
        HttpStatusCode::Unauthorized                =>
            HttpStatus{ code: HttpStatusCode::Unauthorized, reason: "UNAUTHORIZED" },
        HttpStatusCode::PaymentRequired             =>
            HttpStatus{ code: HttpStatusCode::PaymentRequired, reason: "PAYMENT REQUIRED" },
        HttpStatusCode::Forbidden                   =>
            HttpStatus{ code: HttpStatusCode::Forbidden, reason: "FORBIDDEN" },
        HttpStatusCode::NotFound                    =>
            HttpStatus{ code: HttpStatusCode::NotFound, reason: "NOT FOUND" },
        HttpStatusCode::MethodNotAllowed            =>
            HttpStatus{ code: HttpStatusCode::MethodNotAllowed, reason: "METHOD NOT ALLOWED" },
        HttpStatusCode::NotAcceptable               =>
            HttpStatus{ code: HttpStatusCode::NotAcceptable, reason: "NOT ACCEPTABLE" },
        HttpStatusCode::ProxyAuthenticationRequired =>
            HttpStatus{ code: HttpStatusCode::ProxyAuthenticationRequired, reason: "PROXY AUTHENTICATION REQUIRED" },
        HttpStatusCode::RequestTimeout              =>
            HttpStatus{ code: HttpStatusCode::RequestTimeout, reason: "REQUEST TIMEOUT" },
        HttpStatusCode::Conflict                    =>
            HttpStatus{ code: HttpStatusCode::Conflict, reason: "CONFLICT" },
        HttpStatusCode::Gone                        =>
            HttpStatus{ code: HttpStatusCode::Gone, reason: "GONE" },
        HttpStatusCode::LengthRequired              =>
            HttpStatus{ code: HttpStatusCode::LengthRequired, reason: "LENGTH REQUIRED" },
        HttpStatusCode::PreconditionFailed          =>
            HttpStatus{ code: HttpStatusCode::PreconditionFailed, reason: "PRECONDITION FAILED" },
        HttpStatusCode::PayloadTooLarge             =>
            HttpStatus{ code: HttpStatusCode::PayloadTooLarge, reason: "PAYLOAD TOO LARGE" },
        HttpStatusCode::UriTooLong                  =>
            HttpStatus{ code: HttpStatusCode::UriTooLong, reason: "URI TOO LONG" },
        HttpStatusCode::UnsupportedMediaType        =>
            HttpStatus{ code: HttpStatusCode::UnsupportedMediaType, reason: "UNSUPPORTED MEDIA TYPE" },
        HttpStatusCode::RangeNotSatisfiable         =>
            HttpStatus{ code: HttpStatusCode::RangeNotSatisfiable, reason: "RANGE NOT SATISFIABLE" },
        HttpStatusCode::ExpectationFailed           =>
            HttpStatus{ code: HttpStatusCode::ExpectationFailed, reason: "EXPECTATION FAILED" },
        HttpStatusCode::UpgradeRequired             =>
            HttpStatus{ code: HttpStatusCode::UpgradeRequired, reason: "UPGRADE REQUIRED" },
        HttpStatusCode::InternalServerError         =>
            HttpStatus{ code: HttpStatusCode::InternalServerError, reason: "INTERNAL SERVER ERROR" },
        HttpStatusCode::NotImplemented              =>
            HttpStatus{ code: HttpStatusCode::NotImplemented, reason: "NOT IMPLEMENTED" },
        HttpStatusCode::BadGateway                  =>
            HttpStatus{ code: HttpStatusCode::BadGateway, reason: "BAD GATEWAY" },
        HttpStatusCode::ServiceUnavailable          =>
            HttpStatus{ code: HttpStatusCode::ServiceUnavailable, reason: "SERVICE UNAVAILABLE" },
        HttpStatusCode::GatewayTimeout              =>
            HttpStatus{ code: HttpStatusCode::GatewayTimeout, reason: "GATEWAY TIMEOUT" },
        HttpStatusCode::HttpVersionNotSupported     =>
            HttpStatus{ code: HttpStatusCode::HttpVersionNotSupported, reason: "HTTP VERSION NOT SUPPORTED" }
    }
}

pub enum StandardHttpHeaders {
    ContentLength,
}

impl StandardHttpHeaders {
    pub fn from_str(header: &str) -> Option<StandardHttpHeaders> {
        match header {
            "Content-Length" => Some(StandardHttpHeaders::ContentLength),
            _ => None
        }
    }

    pub fn to_str(header: &StandardHttpHeaders) -> &'static str {
        match header {
            StandardHttpHeaders::ContentLength => "Content-Length"
        }
    }
}

// https://tools.ietf.org/html/rfc7231#section-4.3
// https://tools.ietf.org/html/rfc5789
#[derive(Debug, PartialEq, Eq)]
pub enum HttpVerb {
    GET,
    HEAD,
    POST,
    PUT,
    DELETE,
    CONNECT,
    OPTIONS,
    TRACE,
    PATCH
}

impl HttpVerb {
    pub fn from_str(verb: &str) -> Option<HttpVerb> {
        match verb {
            "GET"     => Some(HttpVerb::GET),
            "HEAD"    => Some(HttpVerb::HEAD),
            "POST"    => Some(HttpVerb::POST),
            "PUT"     => Some(HttpVerb::PUT),
            "DELETE"  => Some(HttpVerb::DELETE),
            "CONNECT" => Some(HttpVerb::CONNECT),
            "OPTIONS" => Some(HttpVerb::OPTIONS),
            "TRACE"   => Some(HttpVerb::TRACE),
            "PATCH"   => Some(HttpVerb::PATCH),
            _         => None
        }
    }

    pub fn to_str(v: &HttpVerb) -> &'static str {
        match v {
            HttpVerb::GET     => "GET",
            HttpVerb::HEAD    => "HEAD",
            HttpVerb::POST    => "POST",
            HttpVerb::PUT     => "PUT",
            HttpVerb::DELETE  => "DELETE",
            HttpVerb::CONNECT => "CONNECT",
            HttpVerb::OPTIONS => "OPTIONS",
            HttpVerb::TRACE   => "TRACE",
            HttpVerb::PATCH   => "PATCH"
        }
    }
}


// TODO make stream based
#[derive(Debug)]
pub struct HttpRequest {
    pub verb: HttpVerb,
    pub path: String,
    pub body: String
}

// TODO make stream based
#[derive(Debug)]
pub struct HttpResponse {
    pub status: HttpStatus,
    pub body: String
}

enum ReadMode {
    RequestLine,
    Headers,
    Body
}

fn read_request(mut stream: TcpStream) -> (TcpStream, HttpRequest) {
    let mut buffer: [u8; 4096] = [0; 4096];

    let mut verb_opt: Option<String> = None;
    let mut path_opt: Option<String> = None;
    let mut content_lenth_opt: Option<usize> = None;

    let mut read_mode = ReadMode::RequestLine;
    let mut last_four: [u8; 4] = [0; 4];

    let mut body: String = "".to_owned();
    let length_str = StandardHttpHeaders::to_str(&StandardHttpHeaders::ContentLength).to_lowercase();


    // TODO make this more scalable, this won't work if the chunk size is smaller than the message
    let count = stream
        .read(&mut buffer)
        .expect("Unable to read request from TcpStream");

    let mut j = 0;

    for i in 0..count {
        last_four[3] = last_four[2];
        last_four[2] = last_four[1];
        last_four[1] = last_four[0];
        last_four[0] = buffer[i];

        if last_four[1] == CARRIAGE_RETURN && last_four[0] == LINE_FEED {
            // Two crlfs in a row means start of body
            if last_four[3] == CARRIAGE_RETURN && last_four[2] == LINE_FEED {
                read_mode = ReadMode::Body;

                let is_get = match &verb_opt {
                    Some(v) => v == HttpVerb::to_str(&HttpVerb::GET),
                    None => false,
                };

                if !is_get {
                    let start = i + 1;
                    let end = start + content_lenth_opt.unwrap();
                    body = String::from_utf8_lossy(&buffer[start..end]).to_string();
                }
                break;
            } else {
                let text = String::from_utf8_lossy(&buffer[j..i]);
                let mut tokens = text.split_whitespace();

                match read_mode {
                    ReadMode::RequestLine => {
                        verb_opt = tokens.next().map(|t| t.to_owned());
                        path_opt = tokens.next().map(|t| t.to_owned());
                        read_mode = ReadMode::Headers;
                    },
                    ReadMode::Headers => {
                        let next = tokens.next().unwrap().to_lowercase();

                        if &next[..next.len() - 1] == length_str {
                            let byte_len = tokens.next().unwrap().trim().parse::<usize>().unwrap();
                            content_lenth_opt = Some(byte_len)
                        }
                    }
                    _ => panic!("Impossible")
                }
                j = i;
            }
        }
    }

    (stream, HttpRequest {
        verb: verb_opt.map(|s| HttpVerb::from_str(s.as_str()).unwrap()).unwrap(),
        path: path_opt.unwrap(),
        body: body
    })
}

fn response_to_string(http_response: HttpResponse) -> String {
    let status_line = format!(
        "{} {:?} {}{}",
        HTTP_1_1,
        http_response.status.code,
        http_response.status.reason,
        HTTP_LINE_BREAK
    );

    format!(
        "{}{}",
        status_line,
        http_response.body
    )
}

// TODO streams!
fn handle_connection(stream: TcpStream, router: &'static Router) {
    let (mut stream, request) = read_request(stream);
    let response = router(request);

    stream.write(response_to_string(response).as_bytes()).unwrap();
    stream.flush().unwrap();
}


type Router = fn(HttpRequest) -> HttpResponse;

// TODO make stream based
pub struct HttpServer {
    num_threads: usize
}

impl HttpServer {
    pub fn new(num_threads: usize) -> HttpServer {
        HttpServer {
            num_threads
        }
    }

    pub fn bind(&self, host: &str, port: u32, router: &'static Router) -> Result<(), Box<dyn error::Error>> {
        let addr_str = [host, PORT_SEP, &port.to_string()].concat();
        let listener = TcpListener::bind(&addr_str)?;
        let thread_pool = ThreadPool::new(self.num_threads);

        println!("Listening for http on {}", &addr_str);

        for stream in listener.incoming() {
            let stream = stream.unwrap();

            thread_pool.execute(move || {
                handle_connection(stream, router);
            });
        }
        Ok(())
    }
}

