# Tarpit


Inspired by the post https://nullprogram.com/blog/2019/03/22/.

All credit to Chris Wellons for the initial implementation of both HTTP and SSH tarpits, which I have shamelessly smashed together here, along with his extra credit assignment for an SMTP.

## Current modules
- SSH: the Python implementation of endlessh as outlined on https://nullprogram.com/blog/2019/03/22/
- HTTP: another implementation from the same post.
- SMTP: intial cut of the same concept for an SMTP server. Currently only implements a dodge HELO as per RFC 821
