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

## TODO

### High Priority
- [ ] add tests
- [ ] make into directory module

### Low Priority
- [ ] make cli cleaner, with more emphasis on single user usage


## Development

Currently the scraper in it's initial stages.
Experimenting with different approaches.

Pull requests and issues are accepted.

Currently maintained by Harshith Sairaj 
| [hsa18ms082@iiserkol.ac.in](mailto:hsa18ms082@iiserkol.ac.in)
| [github:pystardust](https://github.com/pystardust/)

## Motive

To give access to SMC data that is accessible only by the manager and
should be accessible by all students.

Main aim is to scrape as a manager account and scrape only the data than
the students should be able to see.

As the manager account has access to sensitive details, this way ensures
the program could be run(after reviewing, testing and authorization).
Extracting relevant data from the files and saving it onto the hard disk/
transferring the data to the appropriate location(studentmess website)
