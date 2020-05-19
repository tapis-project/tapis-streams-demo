From the src folder:

docker build -t tapis/simulator -f Dockerfile-tests .


docker run -v local_path/timelog.txt:/home/tapis/timelog.txt tapis/simulator

