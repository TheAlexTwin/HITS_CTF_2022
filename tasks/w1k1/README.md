# w1k1

## Legend

### w1k1 (Easygi)

#### RU

Реальный проект нашего четверокурсника.

*Флаг лежит в переменных окружения.*

#### EN 

The real project of our fourth-year student.

*Flag is in the server environment.*

### 4m0gu5 (Insane)

#### RU

Похакать этот сервис было довольно просто. 

Давай попробуем найти в локальной сети ещё один HTTP-сервачок?

#### EN 

It was quite easy to hack this service.

Let's try to find another HTTP-server on the local network?

## Description

Small web-service with insecure OS command execution.

## Solutions

### w1k1

Articles are taken from [wikit](https://www.npmjs.com/package/wikit) util,
which is called from OS ```exec``` function.

No input sanitization allows to execute any arbitrary shell command on the server 
with the running application privileges by simply appending malicious payload 
to the end of the harmless article name. 

For instance:

- query ```?search=TSU%20&&%20ls``` will display folder content. 

- query ```?search=TSU%20&&env``` will show you the flag.

### 4m0gu5

At first, we need to get a shell on that server (check previous paragraph).

Legend says that something in a local network is waiting for us, so let's discover it:

1. At first, let's check what we can actually do on that server:

``` $ whoami ```

``` $ ls -lah /bin && ls -lah /usr/bin && ls -lah /usr/sbin ```

We can notice that we run under ```node``` user and have pretty low privileges, but we can execute ``` $ curl``` command, because it's installed here for some reason (maybe healthcheck or something).

2. Let's find out in which network we live:

``` $ ip a```

``` $ route ```

We can see two subnets: 192.168.144.0/20 and 192.168.160.0/20

3. By a little hint in the legend, we know that some host MUST be alive in this area.

We don't have permission to execute ``` $ ping```, but we can build ping on curl utility by knocking on port 80 (like ``` $ curl -Is 192.168.160.1 | grep HTTP | cut -d ' ' -f2```.

After it, we just need to knock to each host in our subnet (e.g. with small bash script). Some of them are actually alive and respond with code 200. After discovery, we just need to check their HTML content. One of these hosts is small http-server which serves us a flag with some curious ascii-art.

## Flags

**HITS{my_f4v0r173_4r71cl3_15_rc3}**

**HITS{4v3r4g3_p3nt35t1ng_3nj0y3r_h3h3}**

## Handout

*Nothing*
