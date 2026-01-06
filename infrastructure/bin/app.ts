#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { DailyBreadStack } from '../lib/dailybread-stack';

const app = new cdk.App();

new DailyBreadStack(app, 'DailyBreadStack', {
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEFAULT_REGION || 'us-east-1',
  },
  description: 'Daily Bread - Nutrition and Meal Planning Application',
});

app.synth();
