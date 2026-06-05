"use client";

import React from "react";

export default function DisclaimerBanner() {
  return (
    <div className="disclaimer-banner">
      <div className="disclaimer-content">
        <span className="warning-badge">Disclaimer</span>
        <p className="disclaimer-text">
          This is a <strong>facts-only</strong> assistant for SBI Mutual Funds. It cannot provide investment advice, personal portfolio details, or performance projections. All information is retrieved directly from official scheme factsheets.
        </p>
      </div>
    </div>
  );
}
