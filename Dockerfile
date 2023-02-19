FROM python:3.9-alpine
ADD api.py .
EXPOSE 8000
CMD ["python", "./api.py"]
