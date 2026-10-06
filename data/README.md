# Data Folder

Place your labeled phishing/legitimate URL CSV here.

The preprocessing script expects:
- one URL column
- one label column

Example:

```csv
url,label
https://example.com,0
http://secure-login-example.com/account,1
```

Accepted label examples include:
- legitimate / benign / safe / good / 0
- phishing / malicious / bad / unsafe / 1 / -1

Do not upload a large or restricted dataset to GitHub unless its license allows redistribution.
