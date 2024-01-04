# if in code space use this to capture the url to login to gcloud
# gcloud auth login 2>&1 | tee out.txt
gcloud auth login
gcloud config set project geo-attractors

# give terraform access to gcloud
gcloud auth application-default login
