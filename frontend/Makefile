DOTENV := npx dotenv
S3_BUCKET = ai-narrator-frontend
BUILD_DIR = dist
PROFILE = default
DISTRIBUTION_ID = $(shell $(DOTENV) -- echo $$CLOUDFRONT_DISTRIBUTION_ID)


all: build deploy invalidate

build:
	@echo "Building the project..."
	@npm run build

deploy:
	@echo "Deploying to S3..."
	@aws s3 sync $(BUILD_DIR)/ s3://$(S3_BUCKET)/ --delete --profile $(PROFILE)

# used when s3 is updated
invalidate:
	@echo "Invalidating CloudFront cache..."
	@aws cloudfront create-invalidation --distribution-id $(DISTRIBUTION_ID) --paths "/*" --profile $(PROFILE)

clean:
	@rm -rf $(CURDIR)/$(BUILD_DIR)
	@echo "Cleaned the build directory."
	

.PHONY: all build deploy clean
