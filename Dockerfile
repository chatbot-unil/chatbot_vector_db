# vectordb/Dockerfile
FROM chromadb/chromadb:latest

# Exposition of the port 3003 for accessing chromadb-server
EXPOSE 3003
CMD ["chromadb-server"]
