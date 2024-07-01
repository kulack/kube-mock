trap 'echo "Bad exit code $?"; exit 1' ERR

if [ -z "$PLATFORM" ]; then
  echo "PLATFORM variable not specified, default to PLATFORM=linux/amd64"
  PLATFORM=--platform=linux/amd64
else
  echo "Building for $PLATFORM"
  PLATFORM=--platform=$PLATFORM
fi

if [ -z "$VERSION" ]; then
  echo "VERSION variable not specified"
  exit 1
fi

if [ -z "$APP" ]; then
  echo "APP variable not specified, default to APP=all (options are all, web, tcp)"
  APP=all
fi

if [ -z "$HUB_USER" ] || [ -z "$HUB_PASS" ] || [ -z "$HUB_REPO" ]; then
  echo "HUB_USER or HUB_PASS or $HUB_REPO not specified, no docker hub push will be done"
  HUB=""
fi

docker login -u $HUB_USER -p $HUB_PASS

if [ "$APP" = "all" ] || [ "$APP" = "web" ]; then
  echo "Building web app..."
  docker build . $PLATFORM -f Dockerfile.web --tag kube-mock-web:latest

  docker tag kube-mock-web:latest $HUB_REPO/kube-mock-web:latest
  docker push $HUB_REPO/kube-mock-web:latest

  docker tag kube-mock-web:latest $HUB_REPO/kube-mock-web:"$VERSION"
  docker push $HUB_REPO/kube-mock-web:"$VERSION"
fi

if [ "$APP" = "all" ] || [ "$APP" = "tcp" ]; then
  echo "Building tcp app..."
  docker build . $PLATFORM -f Dockerfile.tcp --tag kube-mock-tcp:latest

  docker tag kube-mock-tcp:latest $HUB_REPO/kube-mock-tcp:latest
  docker push $HUB_REPO/kube-mock-tcp:latest

  docker tag kube-mock-tcp:latest $HUB_REPO/kube-mock-tcp:"$VERSION"
  docker push $HUB_REPO/kube-mock-tcp:"$VERSION"
fi
