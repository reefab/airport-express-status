FROM python:3.9-alpine
ADD api.py .
EXPOSE 8000
CMD ["python", "./api.py"]
HEALTHCHECK CMD  python -c "import urllib.request as r; import json; exit((json.loads(r.urlopen('http://localhost:8000/health').read())['Status']) != 'OK')"
