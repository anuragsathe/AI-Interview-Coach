provider "aws" {
  region = "ap-south-1"
}

resource "aws_instance" "app_server" {
  ami           = "ami-0f58b397bc5c1f2e8"
  instance_type = "t2.micro"
  key_name      = "ai-key"

  user_data = <<-EOF
  #!/bin/bash
  yum update -y
  yum install -y python3 git

  cd /home/ec2-user
  git clone https://github.com/anuragstathe/AI-Interview-Coach.git

  cd AI-Interview-Coach
  pip3 install -r requirements.txt

  nohup uvicorn app.app:app --host 0.0.0.0 --port 8000 &
  EOF

  tags = {
    Name = "ai-interview-coach"
  }
}
