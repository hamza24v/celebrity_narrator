# David Narrates

## Project Overview

**David Narrates** is an innovative web application designed to provide a unique and engaging experience by narrating user-uploaded images in the iconic style of Sir David Attenborough. The application uses advanced AI technologies to analyze images and generate humorous and insightful narrations, bringing the images to life with a touch of personality and wit.

## Features

- **Image Upload**: Users can upload images directly from their device.
- **AI-Powered Narration**: Utilizes OpenAI's GPT-4o-mini to generate narrations based on the uploaded images.
- **Real-time Feedback**: Provides instant audio feedback with the generated narration.
- **Secure and Scalable**: Deployed on AWS, leveraging EC2, S3, and CloudFront for robust performance and security.

## Tech Stack

- **Frontend**: 
  - **React**: Provides a dynamic and responsive user interface.
  - **Tailwind CSS**: Ensures modern and efficient styling.
  - **Material-UI**: Enhances user experience with sleek and intuitive design components.
  
- **Backend**: 
  - **Django**: Serves as the core backend framework, offering robust API management.
  - **Django Rest Framework**: Simplifies the creation of RESTful APIs.
  - **ElevenLabs API**: Converts text narrations into audio.
  - **OpenAI API**: Generates detailed and humorous narrations for the images.

- **Deployment**:
  - **AWS EC2**: Hosts the backend application, providing scalable compute power.
  - **AWS S3**: Stores frontend assets and user-uploaded images securely.
  - **AWS CloudFront**: Distributes content globally with low latency, ensuring a fast and secure user experience.

## How to Use

1. **Access the Application**: Navigate to the deployed application URL.
2. **Upload an Image**: Click the 'Upload' button to select an image from your device.
3. **Generate Narration**: Once the image is uploaded, the application will process it and generate a narration.
4. **Listen to the Narration**: Click the 'Play' button to hear the narration in the voice of Sir David Attenborough.

## Setup Instructions

### Prerequisites

- Node.js
- Python 3.8+
- AWS Account
- OpenAI API Key
- ElevenLabs API Key

### Backend Setup

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/yourusername/david-narrates.git
   cd david-narrates/backend
   ```

2. **Create a Virtual Environment**:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   Create a `.env` file and add your API keys and other environment variables.

5. **Run Migrations**:
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Start the Server**:
   ```sh
   python manage.py runserver
   ```

### Frontend Setup

1. **Navigate to Frontend Directory**:
   ```sh
   cd ../frontend
   ```

2. **Install Dependencies**:
   ```sh
   npm install
   ```

3. **Start the Development Server**:
   ```sh
   npm start
   ```

### Deployment

#### EC2 Instance

1. **Create an EC2 Instance**: In the AWS Management Console, create an EC2 instance and set up an Elastic IP.
2. **SSH into EC2**:
   ```sh
   ssh -i /path/to/your-key.pem ec2-user@your-ec2-ip
   ```
3. **Deploy Backend**: Upload your backend code to the EC2 instance and run it using a process manager like `gunicorn` or `supervisor`.

#### S3 and CloudFront

1. **Create an S3 Bucket**: In the AWS Management Console, create an S3 bucket and upload your frontend build files.
2. **Set Up CloudFront**: Create a CloudFront distribution pointing to your S3 bucket to serve your frontend content globally.

### Conclusion

**David Narrates** combines cutting-edge AI technologies with a delightful user experience to bring images to life through narration. The project demonstrates proficiency in modern web development, cloud deployment, and AI integration, making it a standout addition to any portfolio.

By following the setup instructions, you can get the application up and running locally or on AWS, showcasing your ability to deploy and manage full-stack applications in a professional environment.