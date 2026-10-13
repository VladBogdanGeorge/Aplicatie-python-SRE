version: '3'

services:
  jenkins:
    #image: jenkins/jenkins:latest
    build: .
    container_name: jenkins
    ports:
      - "8080:8080"
    volumes:
      - jenkins_home:/var/jenkins_home
      - /var/run/docker.sock:/var/run/docker.sock

volumes:
  jenkins_home: # By default, the volume is located at /var/lib/docker/volumes