# M0b1le

## Legend

### Plain (Medium)

#### RU

Наше мобильное приложение умеет скачивать флаги и сдавать их в CTFd в автоматическом режиме.

К сожалению, мы успели реализовать только первую функцию...

#### EN

Our mobile application is able to download flags and submit them to CTFd in automatic mode.

Unfortunately, we managed to implement only the first function...

### Cipher (Hard)

#### RU

... а ещё наш андроид-разработчик настолько ленивый, что не успел дописать функцию дешифрования!

Надеюсь, что он хотя бы в криптографии не накосячил...

#### EN

... and our android-developer is so lazy that he didn't have time to finish the decryption function!

I hope that at least he didn't screw up in cryptography...

## Description

Android app which just downloads two flags (one encrypted and one not).

## Solutions

1. Reverse APK (or sniff traffic from it) and define which API endpoints is it using. Make request to `/api/plaintext_flag` and get your first flag (your User-Agent must contain 'Android' substring).

2. You have AES key, IV and encoded text. What is the problem to write a function to decrypt it and get your second flag?

## Flags

**HITS{fr33_r34l_35t4t3}**

**HITS{y34h_1_kn0w_h0w_t0_u53_AES}**

## Handout

*task.apk*
