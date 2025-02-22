flowchart TD
 subgraph s1["HårdVara"]
        n3["Hårdvara"]
  end
 subgraph s2["vidare utveckling"]
        n4["Vidare utveckling"]
  end
    A1["Ultraljudssensor"] --> B["Raspberry Pi Pico"]
    A2["Ultraljudssensor"] --> E["esp32"]
    E --> C2["LED2"] & D2["Buzzer2"]
    G["MQTT ADAFRUIT IO"] --> E & B & H["Mobil/Dator /Data base"] & n1["ESP32 server"]
    B --> C["LED1"] & D["Buzzer1"]
    F["WiFi"] --> B & E
    n2["Mjukvara"]
    n2@{ shape: text}
    style n4 stroke-width:2px,stroke-dasharray: 2
    style n2 stroke:#FFD600,stroke-width:4px,stroke-dasharray: 0
