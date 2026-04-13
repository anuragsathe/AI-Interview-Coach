provider "aws" {
  region = "ap-south-1"
}

variable "groq_api_key" {
  description = "API Key for Groq"
  type        = string
  sensitive   = true
}

resource "aws_security_group" "app_sg" {
  name        = "ai_interview_coach_sg"
  description = "Allow inbound traffic for web app and SSH"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "app_server" {
  ami           = "ami-0f58b397bc5c1f2e8"
  instance_type = "t3.micro"
  key_name      = "ai-key"

  vpc_security_group_ids = [aws_security_group.app_sg.id]

  user_data = <<-EOF
  #!/bin/bash
  yum update -y
  yum install -y python3 git

  # Set environment variable persistently
  echo "export GROQ_API_KEY=${var.groq_api_key}" >> /etc/profile.d/groq.sh
  export GROQ_API_KEY=${var.groq_api_key}

  cd /home/ec2-user
  git clone https://github.com/anuragstathe/AI-Interview-Coach.git
  cd AI-Interview-Coach
  
  # Install dependencies
  pip3 install -r requirements.txt

  # Run Backend (FastAPI)
  nohup python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
  
  # Run Frontend (Streamlit)
  nohup python3 -m streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0 > frontend.log 2>&1 &
  EOF

  tags = {
    Name = "ai-interview-coach"
  }
}
