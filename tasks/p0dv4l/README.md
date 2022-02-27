# P0dv4l (Medium)

## Legend

### RU

В последнее время наш DNS сервер ну уж слишком сильно барахлит и отвечает через раз.

Мы записали немного траффика с него. Есть время посмотреть?

### EN 

Recently, our DNS server is too much messed up and responds every second time.

We recorded some traffic from it. Do you have some time to check?

## Description

Some base32-encoded short messages is embedded in every third UPD packet.

## Solution

Simply decode those messages extracted with [Wireshark](https://www.wireshark.org/).

E.g. by [open source utils](https://emn178.github.io/online-tools/base32_decode.html).

Flag is written in the last message.

## Flag

**HITS{m3554g3_t0_n0wh3r3}**

## Handout

```task/task.pcapng```
