# Public Access

## Basic Usage

```
usage: smc_scraper.py [-h] username {userreport,logout} ...

positional arguments:
  username             username to authenticate with

options:
  -h, --help           show this help message and exit

commands:
  {userreport,logout}
    userreport         get transactions from rollnumber
    logout             logout of username and remove cookie file

```

- Once logged in the cookie file will be saved for further requests.
- The user could logout, expiring the cookie and deleting the cookie file.
