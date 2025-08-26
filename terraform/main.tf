resource "aws_s3_bucket" "s3_cleaner" {
    bucket ="my-s3-cleaner-demo-bucket"

    tags = {
      Name = "S3CleanerBucket"
      Project = "AWS S3 Cleaner Automation"
    }
}

resource "aws_s3_bucket_lifecycle_configuration" "cleaner-lifecycle" {
    bucket = aws_s3_bucket.s3_cleaner.id

    rule {
      id = "expire-old-objects"
      status = "Enabled"

      expiration {
        days = 3
      }

      filter {
        prefix = ""
      }
    }
}