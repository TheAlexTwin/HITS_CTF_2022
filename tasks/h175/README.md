# H175

## Legend

### IDORable

#### RUS

Так хочется узнать администратора сервиса, но его просто невозможно 
найти в таком огромном количестве пользователей!

#### EN

I really want to know the administrator of the service, but it is simply impossible
to find him in such a HUGE number of users!

### 55T1

#### RUS

Эксплуатация простая как 2×2

*Флаг записан в app.config["SECRET_KEY"]*

#### EN

Exploitation is as simple as 2×2

*Flag is written in app.config["SECRET_KEY"]*

## Description

Damn vulnerable Python 2 project.

Simple service to store CTF task ideas.

## Solutions

1. IDOR allows to read admin profile at <URL>/user/1 (flag is in surname).

2. SSTI in "create private comment form" allows to escape sandbox and 
write arbitary code on the server side. But we only need to read one of
runtime variables, which is much more easy.

## Flags

**HITS{l0v3ly_t3mpl4t35}**

**HITS{4r3_y4_w1nn1ng_50n}**

## Handout

*Nothing*
