# Use alpine to keep the image size small
FROM alpine:latest

# Run as root
USER root

# Copy the main.py file to the root directory
COPY ./main.py /

# Install python3 with no cache to keep the image size small
RUN apk add --no-cache python3

# Create a directory for the output
RUN mkdir /home/output

# Run the main.py file
ENTRYPOINT ["python3", "main.py"]
