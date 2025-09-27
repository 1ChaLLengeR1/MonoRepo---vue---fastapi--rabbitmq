FROM alpine:3.18

# Install PostgreSQL client and dos2unix
RUN apk add --no-cache postgresql-client bash dos2unix

# Create working directory
WORKDIR /migration/scripts

# Copy files maintaining original structure
COPY database/ ../database/
COPY scripts/*.sh ./
COPY .env ../.env

# Fix line endings and make scripts executable
RUN dos2unix ../.env ./*.sh && \
    chmod +x ./*.sh

# Default command
CMD ["bash"]