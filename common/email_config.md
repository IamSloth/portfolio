# Email Config

## Gmail SMTP

| Key | Value |
|-----|-------|
| SMTP Server | smtp.gmail.com:587 (STARTTLS) |
| Account | ssujklim@gmail.com |
| App Password | byhf kmcf wefr ycoi |
| Script | applications/06_sk_energy/scripts/send_email.py |

## Usage

```python
import smtplib
from email.mime.multipart import MIMEMultipart

smtp = smtplib.SMTP("smtp.gmail.com", 587)
smtp.starttls()
smtp.login("ssujklim@gmail.com", "byhf kmcf wefr ycoi")
```
