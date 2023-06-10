// use reqwest::{Client, Proxy};
// use tokio;
//
// #[tokio::main]
// async fn main() {
//     println!("Hello, world!");
//     let proxy = Proxy::all("socks5://127.0.0.1:9050").unwrap();
//
//     let client = Client::builder()
//         .proxy(proxy)
//         .build()
//         .unwrap();
//
//     fetch(&client, "http://gkcns4d3453llqjrksxdijfmmdjpqsykt6misgojxlhsnpivtl3uwhqd.onion")
//         .await;
// }
//
// pub async fn fetch(cl: &Client, url: &str) {
//     let resp = match cl.get(url).send().await {
//         Ok(resp) => resp,
//         Err(err) => {
//             println!("req failed!: {}", err);
//             return;
//         }
//     };
//     println!("resp: {:?}", resp);
// }
use std::io::prelude::*;
use tor_stream::TorStream;

fn main() {
    let mut stream =
        TorStream::connect("gkcns4d3453llqjrksxdijfmmdjpqsykt6misgojxlhsnpivtl3uwhqd.onion:80")
            .expect("Failed to connect");

    // The stream can be used like a normal TCP stream

    stream
        .write_all(b"GET / HTTP/1.1\r\nConnection: Close\r\nHost:gkcns4d3453llqjrksxdijfmmdjpqsykt6misgojxlhsnpivtl3uwhqd.onion:80\r\n\r\n")
        .expect("Failed to send request");

    // If you want the raw stream, call `into_inner()`

    let mut stream = stream.into_inner();

    let mut buf = String::new();
    stream
        .read_to_string(&mut buf)
        .expect("Failed to read response");

    println!("Server response:\n{}", buf);
}
