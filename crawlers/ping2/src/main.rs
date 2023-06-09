use reqwest::{Client, Proxy};
use tokio;

#[tokio::main]
async fn main() {
    println!("Hello, world!");
    let proxy = Proxy::all("socks5://127.0.0.1:9050").unwrap();

    let client = Client::builder()
        .proxy(proxy)
        .build()
        .unwrap();

    fetch(&client, "http://gkcns4d3453llqjrksxdijfmmdjpqsykt6misgojxlhsnpivtl3uwhqd.onion/")
        .await;
}

pub async fn fetch(cl: &Client, url: &str) {
    let resp = match cl.get(url).send().await {
        Ok(resp) => resp,
        Err(err) => {
            println!("req failed!: {}", err);
            return;
        }
    };
    println!("resp: {:?}", resp);
}
