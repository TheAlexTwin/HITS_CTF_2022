# R3p0rt 1t!

## Legend

### Bip Bup Bip (Easy)

#### RU

Когда разработчик запрещает индексирование страниц, в мире плачет один поисковый робот.

#### EN

When a developer prohibits web-pages indexing, one search-robot in the world cries.

### X55ed (Hard)

#### RU

Что может быть проще, чем стащить печеньку админа?..

*Администратор посещает страницу /reports и смотрит все существующие записи каждые три минуты.*

#### EN

What could be easier than stealing the adminstrator cookie?..

*Administrator is visising /reports page and clicking on each report for every 180 seconds.*

### R3d1s (Medium)

#### RU

Они обещали мне, что использование NoSQL хранилищ намного безопаснее!

Ну, я вот и использую...

#### EN

They promised me that using NoSQL storage is much safer!

Well, that's the reason why I'm using it...

## Description

A small service for sending complaints and problems. 

Has a vulnerability to XSS and an injection in Redis.

## Solutions

1. Just view /robots.txt and proceed to indexing-restricted file. Flag is encrypted with ROT13.

2. ```redis_sploit.py```

3. ```xss_sploit.py```

## Flags

**HITS{4v3r4g3_cr4wl1ng_3nj03r}**

**HITS{m4mk1n_h4ck3r}**

**HITS{pl3453_d0_n0t_try_t0_r3wr1t3_m3_51r}**

## Handout

*Nothing*
