# Launch Checklist - 24 Hours to Revenue

## Phase 1: Setup (2 hours)

- [ ] Clone repo locally
- [ ] Test locally: `docker-compose up`
- [ ] Test with sample DICOM file
- [ ] Verify landing page looks good
- [ ] Create Hugging Face account (if deploying there)

## Phase 2: Deploy (1 hour)

Choose one:

### Option A: Hugging Face Spaces (Easiest)
- [ ] Create new Space on huggingface.co
- [ ] Connect GitHub repo
- [ ] Wait for automatic build (5-10 min)
- [ ] Test deployed version
- [ ] Update landing page with HF Space URL

### Option B: AWS EC2 (Production)
- [ ] Launch g4dn.xlarge instance
- [ ] SSH in and run Docker
- [ ] Set up nginx reverse proxy
- [ ] Point domain (GoDaddy/Namecheap)
- [ ] Estimate: $500-1000/month

### Option C: Local + Ngrok (Testing)
- [ ] Run docker-compose locally
- [ ] Install ngrok
- [ ] `ngrok http 8000`
- [ ] Get public URL for testing

## Phase 3: Marketing (1 hour)

### Reddit Launch
- [ ] Join r/radiology, r/MachineLearning, r/HealthTech
- [ ] Write launch post: "Built a 2-click medical image segmentation tool"
- [ ] Include: Problem → Solution → Live demo link → How to use
- [ ] Post to 3-5 relevant subreddits

### Direct Outreach
- [ ] Find 20 hospital IT director emails (LinkedIn)
- [ ] Template email:
  ```
  Subject: 30-second liver segmentation tool (radiology teams)
  
  Hi [Name],
  
  I built a tool that segments CT scans in 30 seconds. No software to install.
  
  Live demo: [URL]
  Video: [2-min demo]
  
  Works for: Liver, lung, spleen
  Accuracy: 95%+
  Cost: $99/month
  
  Would your team benefit?
  
  [Your name]
  [Phone]
  ```

### Twitter/X Launch
- [ ] Thread: Problem → Solution → How it works → Demo video
- [ ] Tag: #radiology #AI #medtech
- [ ] Get 10-20 relevant follows to engage

### ProductHunt (Optional)
- [ ] Post in AI/Healthcare categories
- [ ] Prepare punchy tagline: "Segment medical images in 30 seconds, no install"
- [ ] Upload demo video

## Phase 4: Initial Sales (4-6 hours)

- [ ] Set up Stripe account
- [ ] Create simple pricing page
- [ ] Monitor support emails
- [ ] Fix bugs quickly (same day)
- [ ] Collect feedback for roadmap

## Phase 5: Day 2+ (Ongoing)

- [ ] Monitor uptime: `https://your-domain/health`
- [ ] Respond to inquiries within 1 hour
- [ ] Add 1 new feature per week based on feedback
- [ ] Post weekly updates on Twitter

---

## First Customer Milestones

| Time | Goal |
|------|------|
| Hour 24 | 5 demo users |
| Day 3 | 1 paying customer |
| Week 1 | 5 paying customers ($500 MRR) |
| Month 1 | 20 customers ($2K MRR) |
| Month 3 | 50+ customers ($5K+ MRR) |

---

## Revenue Math

At $99/month subscription:
- 50 customers = $5,000/month
- 100 customers = $10,000/month
- 200 customers = $20,000/month

Target: 100 paying customers in 6 months = $1000 MRR → Scale to $2K+ MRR

---

## Sample Support Email Template

```
Thank you for trying MedImaging!

If you have questions:
- Check docs: [URL]
- Video tutorial: [URL]
- Email support within 24 hours

Got feedback? Reply to this email.

- [Your name]
```

