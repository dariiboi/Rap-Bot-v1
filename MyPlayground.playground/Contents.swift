//: Playground - noun: a place where people can play

import PlaygroundSupport
import Foundation

let url = URL(string: "http://localhost:8080/generate?seedWord=jon")

let task = URLSession.shared.dataTask(with: url!) { data, response, error in
    guard error == nil else {
        print(error!)
        return
    }
    guard let data = data else {
        print("Data is empty")
        return
    }
    
    let json = try! JSONSerialization.jsonObject(with: data, options: [])
    //let string = String(data: data, encoding: .utf8)
    print(json)
}

task.resume()
PlaygroundPage.current.needsIndefiniteExecution = true
