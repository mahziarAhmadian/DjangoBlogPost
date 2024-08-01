# Dockerfiles/redis/Dockerfile
FROM redis:latest

# Set the command to run Redis with the specified options
CMD ["redis-server", "--save", "60", "1", "--loglevel", "warning"]

EXPOSE 6379