name: "Generate and Upload SBOM to https://sbom.sh"

on: [push, pull_request, workflow_dispatch]

jobs:
  generate_sbom:
    runs-on: ubuntu-latest
    name: "SBOM Generation"
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v2
      
      - name: Generate SBOM
        id: sbom_generation
        run: |
          RESPONSE=$(docker run --rm -v ${{ github.workspace }}:/app codenotary/sbom.sh:latest grypefs)
          echo "SBOM_RESPONSE=$RESPONSE" >> $GITHUB_ENV
      
      - name: Extract ShareUrl
        run: |
          SHARE_URL=$(echo $SBOM_RESPONSE | jq -r '.ShareUrl')
          echo "SBOM_SHARE_URL=$SHARE_URL" >> $GITHUB_ENV
      
      - name: Output SBOM URL
        run: echo "The SBOM can be found at $SBOM_SHARE_URL"    
      
      - name: Comment on Pull Request
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v3
        with:
          github-token: ${{secrets.GITHUB_TOKEN}}
          script: |
            github.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: "Generated SBOM is available at: ${{ env.SBOM_SHARE_URL }}"
            })
