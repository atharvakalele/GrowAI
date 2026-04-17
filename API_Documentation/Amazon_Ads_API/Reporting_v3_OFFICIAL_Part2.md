# Amazon Ads Reporting API v3 - Official Documentation Part 2
**Source:** Official Amazon Advertising documentation (manually copied by Msir)
**Date Captured:** 13 April 2026
**API Version:** Ads Reporting v3 / v1 Unified Reporting
**Our Endpoint:** advertising-api-eu.amazon.com
**Our Profile ID:** 42634532240933

## Report Types in This File:
- Search Term: spSearchTerm, sbSearchTerm
- Targeting: spTargeting, sbTargeting, sdTargeting, stTargeting
- Placement: sbCampaignPlacement (SP uses campaign groupBy, no separate report)
- Purchased Product: spPurchasedProduct, sbPurchasedProduct, sdPurchasedProduct
- Gross and Invalid Traffic: spGrossAndInvalids, sbGrossAndInvalids, sdGrossAndInvalids
- Full Columns/Metrics Reference (400+ metrics)

## Important Corrections:
- spPlacement does NOT exist as separate report - use spCampaigns with groupBy: campaignPlacement
- sbCampaignPlacement is the correct reportTypeId (not sbPlacement)
- spGrossAndInvalids is correct (not spGrossAndInvalidTraffic)
- sbSearchTerm and sbTargeting are in PREVIEW status

---

In this document

Configurations
Sponsored Products
Base metrics
Group by searchTerm
Sponsored Brands
Base metrics
Group by searchTerm
Sample calls
Sponsored Products: Targeting expressions only
Sponsored Products: Keywords only
Sponsored Brands
Search term reports
Search term reports contain search term performance metrics broken down by targeting expressions and keywords. Note that search term reports only include impressions that resulted in at least one ad click. Use the keywordType filter to include either targeting expressions or keywords in your report.

 Note
If a placement does not have a search keyword associated with it on a product detail page, the search term in the report will be an asterisk *.
Configurations
Configuration	Sponsored Products	Sponsored Brands
reportTypeId	spSearchTerm	sbSearchTerm
Maximum date range	31 days	31 days
Data retention	95 days	60 days
timeUnit	SUMMARY or DAILY	SUMMARY or DAILY
groupBy	searchTerm	searchTerm
format	GZIP_JSON	GZIP_JSON
Sponsored Products
Base metrics
impressions, addToList, qualifiedBorrows, royaltyQualifiedBorrows, clicks, costPerClick, clickThroughRate, cost, purchases1d, purchases7d, purchases14d, purchases30d, purchasesSameSku1d, purchasesSameSku7d, purchasesSameSku14d, purchasesSameSku30d, unitsSoldClicks1d, unitsSoldClicks7d, unitsSoldClicks14d, unitsSoldClicks30d, sales1d, sales7d, sales14d, sales30d, attributedSalesSameSku1d, attributedSalesSameSku7d, attributedSalesSameSku14d, attributedSalesSameSku30d, unitsSoldSameSku1d, unitsSoldSameSku7d, unitsSoldSameSku14d, unitsSoldSameSku30d, kindleEditionNormalizedPagesRead14d, kindleEditionNormalizedPagesRoyalties14d, salesOtherSku7d, unitsSoldOtherSku7d, acosClicks7d, acosClicks14d, roasClicks7d, roasClicks14d, keywordId, keyword, campaignBudgetCurrencyCode, date, startDate, endDate, portfolioId, searchTerm, campaignName, campaignId, campaignBudgetType, campaignBudgetAmount, campaignStatus, keywordBid, adGroupName, adGroupId, keywordType, matchType, targeting, adKeywordStatus

Group by searchTerm
Additional metrics: adKeywordStatus

Filters:

keywordType (values: BROAD, PHRASE, EXACT, TARGETING_EXPRESSION, TARGETING_EXPRESSION_PREDEFINED)
Sponsored Brands
 Note
This report is currently available in preview. During the preview period, data related to Sponsored Brands campaigns with flag isMultiAdGroupsEnabled set to FALSE won’t be available. Once version 3 reporting supports all Sponsored Brands campaigns, we will announce general availability in the release notes.
Base metrics
adGroupId, adGroupName, addToList, addToListFromClicks, qualifiedBorrows, qualifiedBorrowsFromClicks, royaltyQualifiedBorrows, royaltyQualifiedBorrowsFromClicks, campaignBudgetAmount, campaignBudgetCurrencyCode, campaignBudgetType, campaignId, campaignName, campaignStatus, clicks, cost, costType, date, endDate, impressions, keywordBid, keywordId, keywordText, kindleEditionNormalizedPagesRead14d, kindleEditionNormalizedPagesRoyalties14d, matchType, purchases, purchasesClicks, sales, salesClicks, searchTerm, startDate, unitsSold, video5SecondViewRate, video5SecondViews, videoCompleteViews, videoFirstQuartileViews, videoMidpointViews, videoThirdQuartileViews, videoUnmutes, viewabilityRate, viewableImpressions, viewClickThroughRate

Group by searchTerm
Additional metrics: adKeywordStatus

Filters:

keywordType (values: BROAD, PHRASE, EXACT, TARGETING_EXPRESSION, TARGETING_EXPRESSION_PREDEFINED)
Sample calls
Sponsored Products: Targeting expressions only
curl --location --request POST 'https://advertising-api.amazon.com/reporting/reports' \
--header 'Content-Type: application/vnd.createasyncreportrequest.v3+json' \
--header 'Amazon-Advertising-API-ClientId: amzn1.application-oa2-client.xxxxxxxx' \
--header 'Amazon-Advertising-API-Scope: xxxxxxxx' \
--header 'Authorization: Bearer Atza|xxxxxxxxx' \
--data-raw '{
    "name":"SP search term report 7/5-7/10",
    "startDate":"2022-07-05",
    "endDate":"2022-07-10",
    "configuration":{
        "adProduct":"SPONSORED_PRODUCTS",
        "groupBy":["searchTerm"],
        "columns":["impressions","clicks","cost","campaignId","adGroupId","date","targeting","searchTerm","keywordType","keywordId"],
        "filters": [
            {
                "field": "keywordType",
                "values": [
                    "TARGETING_EXPRESSION",
                    "TARGETING_EXPRESSION_PREDEFINED"
                ]
            }
        ],
        "reportTypeId":"spSearchTerm",
        "timeUnit":"DAILY",
        "format":"GZIP_JSON"
    }
}'
Sponsored Products: Keywords only
curl --location --request POST 'https://advertising-api.amazon.com/reporting/reports' \
--header 'Content-Type: application/vnd.createasyncreportrequest.v3+json' \
--header 'Amazon-Advertising-API-ClientId: amzn1.application-oa2-client.xxxxxxxx' \
--header 'Amazon-Advertising-API-Scope: xxxxxxxx' \
--header 'Authorization: Bearer Atza|xxxxxxxxx' \
--data-raw '{
    "name":"SB search terms report 7/5-7/10",
    "startDate":"2022-07-05",
    "endDate":"2022-07-10",
    "configuration":{
        "adProduct":"SPONSORED_PRODUCTS",
        "groupBy":["searchTerm"],
        "columns":["impressions","clicks","cost","campaignId","adGroupId","startDate","endDate","keywordType","keyword","matchType","keywordId","searchTerm"],
        "filters": [
            {
                "field": "keywordType",
                "values": [
                    "BROAD",
                    "PHRASE",
                    "EXACT"
                ]
            }
        ],
        "reportTypeId":"spSearchTerm",
        "timeUnit":"SUMMARY",
        "format":"GZIP_JSON"
    }
}'
Sponsored Brands
curl --location 'https://advertising-api.amazon.com/reporting/reports' \
--header 'Content-Type: application/vnd.createasyncreportrequest.v3+json' \
--header 'Amazon-Advertising-API-ClientId: amzn1.application-oa2-client.xxxxxxxx' \
--header 'Amazon-Advertising-API-Scope: xxxxxxxx' \
--header 'Authorization: Bearer Atza|xxxxxxxx' \
--data '{
    "name": "SP search terms report 9/5-9/10",
    "startDate": "2023-09-05",
    "endDate": "2023-09-10",
    "configuration": {
        "adProduct": "SPONSORED_BRANDS",
        "groupBy": [
            "searchTerm"
        ],
        "columns": [
            "impressions",
            "clicks",
            "cost",
            "campaignId",
            "adGroupId",
            "startDate",
            "endDate",
            "matchType",
            "keywordId",
            "searchTerm"
        ],
        "filters": [
            {
                "field": "keywordType",
                "values": [
                    "BROAD",
                    "PHRASE",
                    "EXACT"
                ]
            }
        ],
        "reportTypeId": "sbSearchTerm",
        "timeUnit": "SUMMARY",
        "format": "GZIP_JSON"
    }
}'

In this document

Configurations
Requesting keywords vs. targets
Sponsored Products
Base metrics
Group by targeting
Sponsored Brands
Base metrics
Group by targeting
Sponsored Display
Base metrics
Group by targeting
Group by matchedTarget
Sponsored Television
Base metrics
Group by campaign
Group by adGroup
Group by targeting
Sample calls
Sponsored Products: Targeting expressions only
Sponsored Products: Keywords only
Sponsored Brands: Keywords only
Targeting reports
Targeting reports contain performance metrics broken down by both targeting expressions and keywords.

Configurations
Configuration	Sponsored Products	Sponsored Brands	Sponsored Display	Sponsored Television
reportTypeId	spTargeting	sbTargeting	sdTargeting	stTargeting
Maximum date range	31 days	31 days	31 days	31 days
Data retention	95 days	60 days	65 days	95 days
timeUnit	SUMMARY or DAILY	SUMMARY or DAILY	SUMMARY or DAILY	SUMMARY or DAILY
groupBy	targeting	targeting	targeting, matchedTarget	campaign, adGroup, or targeting
format	GZIP_JSON	GZIP_JSON	GZIP_JSON	GZIP_JSON
 Note
Targeting reports are not supported for Sponsored TV non-endemic advertisers.
Requesting keywords vs. targets
To see only targeting expressions, set the keywordType filter to TARGETING_EXPRESSION and TARGETING_EXPRESSION_PREDEFINED. To see only keywords, set the keywordType filter to BROAD, PHRASE, and EXACT.

Sponsored Products
Base metrics
impressions, addToList, qualifiedBorrows, royaltyQualifiedBorrows, clicks, costPerClick, clickThroughRate, cost, purchases1d, purchases7d, purchases14d, purchases30d, purchasesSameSku1d, purchasesSameSku7d, purchasesSameSku14d, purchasesSameSku30d, unitsSoldClicks1d, unitsSoldClicks7d, unitsSoldClicks14d, unitsSoldClicks30d, sales1d, sales7d, sales14d, sales30d, attributedSalesSameSku1d, attributedSalesSameSku7d, attributedSalesSameSku14d, attributedSalesSameSku30d, unitsSoldSameSku1d, unitsSoldSameSku7d, unitsSoldSameSku14d, unitsSoldSameSku30d, kindleEditionNormalizedPagesRead14d, kindleEditionNormalizedPagesRoyalties14d, salesOtherSku7d, unitsSoldOtherSku7d, acosClicks7d, acosClicks14d, roasClicks7d, roasClicks14d, keywordId, keyword, campaignBudgetCurrencyCode, date, startDate, endDate, portfolioId, campaignName, campaignId, campaignBudgetType, campaignBudgetAmount, campaignStatus, keywordBid, adGroupName, adGroupId, keywordType, matchType, targeting, topOfSearchImpressionShare

Group by targeting
Additional metrics: adKeywordStatus

Filters:

adKeywordStatus (values: ENABLED,PAUSED,ARCHIVED)
keywordType (values: BROAD, PHRASE, EXACT, TARGETING_EXPRESSION, TARGETING_EXPRESSION_PREDEFINED)
Sponsored Brands
 Note
This report currently available in preview. During the preview period, data related to Sponsored Brands campaigns with flag isMultiAdGroupsEnabled=False won’t be available. Once version 3 reporting supports all Sponsored Brands campaigns, we will announce general availability in the release notes.
Base metrics
addToCart, addToCartClicks, addToCartRate, adGroupId, adGroupName, addToList, addToListFromClicks, qualifiedBorrows, qualifiedBorrowsFromClicks, royaltyQualifiedBorrows, royaltyQualifiedBorrowsFromClicks, brandedSearches, brandedSearchesClicks, campaignBudgetAmount, campaignBudgetCurrencyCode, campaignBudgetType, campaignId, campaignName, campaignStatus, clicks, cost, costType, date, detailPageViews, detailPageViewsClicks, eCPAddToCart, endDate, impressions, keywordBid, keywordId, adKeywordStatus, keywordText, keywordType, matchType, newToBrandDetailPageViewRate, newToBrandDetailPageViews, newToBrandDetailPageViewsClicks, newToBrandECPDetailPageView, newToBrandPurchases, newToBrandPurchasesClicks, newToBrandPurchasesPercentage, newToBrandPurchasesRate, newToBrandSales, newToBrandSalesClicks, newToBrandSalesPercentage, newToBrandUnitsSold, newToBrandUnitsSoldClicks, newToBrandUnitsSoldPercentage, purchases, purchasesClicks, purchasesPromoted, sales, salesClicks, salesPromoted, startDate, targetingExpression, targetingId, targetingText, targetingType, topOfSearchImpressionShare, unitsSold

Group by targeting
Additional metrics: N/A

Filters:

adKeywordStatus (values: ENABLED,PAUSED,ARCHIVED)
keywordType (values: BROAD, PHRASE, EXACT, TARGETING_EXPRESSION, TARGETING_EXPRESSION_PREDEFINED, THEME)
Sponsored Display
Base metrics
addToCart, addToCartClicks, addToCartRate, addToCartViews, adGroupId, adGroupName, addToList, addToListFromClicks, addToListFromViews, qualifiedBorrows, qualifiedBorrowsFromClicks, qualifiedBorrowsFromViews, royaltyQualifiedBorrows, royaltyQualifiedBorrowsFromClicks, royaltyQualifiedBorrowsFromViews, brandedSearches, brandedSearchesClicks, brandedSearchesViews, brandedSearchRate, campaignBudgetCurrencyCode, campaignId, campaignName, clicks, cost, date, detailPageViews, detailPageViewsClicks, eCPAddToCart, eCPBrandSearch, endDate, impressions, impressionsViews, kindleEditionNormalizedPagesRead, kindleEditionNormalizedPagesReadFromClicks, kindleEditionNormalizedPagesReadFromViews, kindleEditionNormalizedPagesRoyalties, kindleEditionNormalizedPagesRoyaltiesFromClicks, kindleEditionNormalizedPagesRoyaltiesFromViews, newToBrandPurchases, newToBrandPurchasesClicks, newToBrandSales, newToBrandSalesClicks, newToBrandUnitsSold, newToBrandUnitsSoldClicks, purchases, purchasesClicks, purchasesPromotedClicks, sales, salesClicks, salesPromotedClicks, startDate, targetingExpression, targetingId, targetingText, unitsSold, unitsSoldClicks, videoCompleteViews, videoFirstQuartileViews, videoMidpointViews, videoThirdQuartileViews, videoUnmutes, viewabilityRate, viewClickThroughRate

Group by targeting
Additional metrics: adKeywordStatus, newToBrandDetailPageViewClicks, newToBrandDetailPageViewRate, newToBrandDetailPageViews, newToBrandDetailPageViewViews, newToBrandECPDetailPageView

Filters: N/A

Group by matchedTarget
Additional metrics: matchedTargetAsin

Filters: N/A

Sponsored Television
Base metrics
addToCart, addToCartClicks, addToCartViews, brandedSearches, brandedSearchesClicks, brandedSearchesViews, clicks, clickThroughRate, cost, costPerThousandImpressions, date, detailPageViews, detailPageViewsClicks, detailPageViewsViews, endDate, impressions, keyword, keywordBid, keywordId, keywordType, matchType, newToBrandDetailPageViewClicks, newToBrandDetailPageViews, newToBrandDetailPageViewViews, newToBrandPurchases, newToBrandPurchasesClicks, newToBrandPurchasesViews, newToBrandSales, newToBrandSalesClicks, newToBrandSalesViews, portfolioId, purchases, purchasesClicks, purchasesViews, roas, sales, salesClicks, salesViews, startDate, targetingText, unitsSold, unitsSoldClicks, unitsSoldViews, videoCompleteViews, videoFirstQuartileViews, videoMidpointViews, videoThirdQuartileViews

Group by campaign

Additional metrics: campaignName, campaignId, campaignStatus, campaignBudgetAmount, campaignBudgetType, campaignBudgetCurrencyCode

Filters:

campaignStatus (values: ENABLED, PAUSED, ARCHIVED)
Group by adGroup

Additional metrics: adGroupName, adGroupId, adStatus

Filters:

adStatus (values: ENABLED, PAUSED, ARCHIVED)
Group by targeting
Additional metrics: adKeywordStatus

Filters:

adKeywordStatus (values: ENABLED,PAUSED,ARCHIVED)
Sample calls
Sponsored Products: Targeting expressions only
curl --location 'https://advertising-api.amazon.com/reporting/reports' \
--header 'Content-Type: application/vnd.createasyncreportrequest.v3+json' \
--header 'Amazon-Advertising-API-ClientId: amzn1.application-oa2-client.xxxxxx' \
--header 'Amazon-Advertising-API-Scope: xxxxxx' \
--header 'Authorization: Bearer Atza|xxxxxxx' \
--data '{
    "name": "SP targeting report 9/5-9/10",
    "startDate": "2023-09-05",
    "endDate": "2023-09-10",
    "configuration": {
        "adProduct": "SPONSORED_PRODUCTS",
        "groupBy": [
            "targeting"
        ],
        "columns": [
            "adGroupId",
            "campaignId",
            "targeting",
            "keywordId",
            "matchType",
            "impressions",
            "clicks",
            "cost",
            "purchases1d",
            "purchases7d",
            "purchases14d",
            "purchases30d",
            "startDate",
            "endDate"
        ],
        "filters": [
            {
                "field": "keywordType",
                "values": [
                    "TARGETING_EXPRESSION",
                    "TARGETING_EXPRESSION_PREDEFINED"
                ]
            }
        ],
        "reportTypeId": "spTargeting",
        "timeUnit": "SUMMARY",
        "format": "GZIP_JSON"
    }
}'
Sponsored Products: Keywords only
curl --location 'https://advertising-api.amazon.com/reporting/reports' \
--header 'Content-Type: application/vnd.createasyncreportrequest.v3+json' \
--header 'Amazon-Advertising-API-ClientId: amzn1.application-oa2-client.xxxxxxxxx' \
--header 'Amazon-Advertising-API-Scope: xxxxxxx' \
--header 'Authorization: Bearer Atza|xxxxxxxxx' \
--data '{
    "name": "SP keywords report 9/5-9/10",
    "startDate": "2023-09-05",
    "endDate": "2023-09-10",
    "configuration": {
        "adProduct": "SPONSORED_PRODUCTS",
        "groupBy": [
            "targeting"
        ],
        "columns": [
            "adGroupId",
            "campaignId",
            "keywordId",
            "matchType",
            "keyword",
            "impressions",
            "clicks",
            "cost",
            "purchases1d",
            "purchases7d",
            "purchases14d",
            "purchases30d",
            "startDate",
            "endDate"
        ],
        "filters": [
            {
                "field": "keywordType",
                "values": [
                    "BROAD",
                    "PHRASE",
                    "EXACT"
                ]
            }
        ],
        "reportTypeId": "spTargeting",
        "timeUnit": "SUMMARY",
        "format": "GZIP_JSON"
    }
}'
Sponsored Brands: Keywords only
curl --location 'https://advertising-api.amazon.com/reporting/reports' \
--header 'Content-Type: application/vnd.createasyncreportrequest.v3+json' \
--header 'Amazon-Advertising-API-ClientId: amzn1.application-oa2-client.xxxxxx' \
--header 'Amazon-Advertising-API-Scope: xxxxxxx' \
--header 'Authorization: Bearer Atza|xxxxxxx' \
--data '{
    "name": "SB keywords report 9/5-9/10",
    "startDate": "2023-09-05",
    "endDate": "2023-09-10",
    "configuration": {
        "adProduct": "SPONSORED_BRANDS",
        "groupBy": [
            "targeting"
        ],
        "columns": [
            "adGroupId",
            "campaignId",
            "keywordId",
            "matchType",
            "keywordText",
            "impressions",
            "clicks",
            "cost",
            "startDate",
            "endDate"
        ],
        "filters": [
            {
                "field": "keywordType",
                "values": [
                    "BROAD",
                    "PHRASE",
                    "EXACT"
                ]
            }
        ],
        "reportTypeId": "sbTargeting",
        "timeUnit": "SUMMARY",
        "format": "GZIP_JSON"
    }
}'

In this document

Configurations
Sponsored Brands
Base metrics
Group by campaignPlacement
Group by campaign
Sample calls
Sponsored Brands: campaign placement summary report
Placement reports
Placement reports contain performance data broken down by ad placement.

 Note
For Sponsored Products, there is not a separate placement report. You can get placement-level data using the 'campaignPlacement' groupBy in a campaign report.
Configurations
Configuration	Sponsored Brands
reportTypeId	sbCampaignPlacement
Maximum date range	31 days
Data retention	60 days
timeUnit	SUMMARY or DAILY
groupBy	campaign
format	GZIP_JSON
Sponsored Brands
 Note
This report is currently available in preview. During the preview period, data related to Sponsored Brands campaigns with flag isMultiAdGroupsEnabled set to FALSE won’t be available. Once version 3 reporting supports all Sponsored Brands campaigns, we will announce general availability in the release notes.
Base metrics
addToCart, addToCartClicks, addToCartRate, addToList, addToListFromClicks, qualifiedBorrows, qualifiedBorrowsFromClicks, royaltyQualifiedBorrows, royaltyQualifiedBorrowsFromClicks, brandedSearches, brandedSearchesClicks, campaignBudgetAmount, campaignBudgetCurrencyCode, campaignBudgetType, campaignId, campaignName, campaignStatus, clicks, cost, costType, date, detailPageViews, detailPageViewsClicks, eCPAddToCart, endDate, impressions, kindleEditionNormalizedPagesRead14d, kindleEditionNormalizedPagesRoyalties14d, newToBrandDetailPageViewRate, newToBrandDetailPageViews, newToBrandDetailPageViewsClicks, newToBrandECPDetailPageView, newToBrandPurchases, newToBrandPurchasesClicks, newToBrandPurchasesPercentage, newToBrandPurchasesRate, newToBrandSales, newToBrandSalesClicks, newToBrandSalesPercentage, newToBrandUnitsSold, newToBrandUnitsSoldClicks, newToBrandUnitsSoldPercentage, purchases, purchasesClicks, purchasesPromoted, sales, salesClicks, salesPromoted, startDate, unitsSold, unitsSoldClicks, video5SecondViewRate, video5SecondViews, videoCompleteViews, videoFirstQuartileViews, videoMidpointViews, videoThirdQuartileViews, videoUnmutes, viewabilityRate, viewableImpressions, viewClickThroughRate

Group by campaignPlacement
Additional metrics: placementClassification

Group by campaign
Additional metrics: N/A

Sample calls
Sponsored Brands: campaign placement summary report
curl --location 'https://advertising-api.amazon.com/reporting/reports' \
--header 'Content-Type: application/vnd.createasyncreportrequest.v3+json' \
--header 'Amazon-Advertising-API-ClientId: amzn1.application-oa2-client.xxxxxxxxx' \
--header 'Amazon-Advertising-API-Scope: xxxxxxx' \
--header 'Authorization: Bearer Atza|xxxxxxxx' \
--data '{
    "name": "SB placement report 9/5-9/10",
    "startDate": "2023-09-05",
    "endDate": "2023-09-10",
    "configuration": {
        "adProduct": "SPONSORED_BRANDS",
        "groupBy": [
            "campaignPlacement"
        ],
        "columns": [
            "impressions",
            "clicks",
            "cost",
            "campaignId",
            "placementClassification",
            "startDate",
            "endDate"
        ],
        "reportTypeId": "sbCampaignPlacement",
        "timeUnit": "SUMMARY",
        "format": "GZIP_JSON"
    }
}'

In this document

Configurations
Sponsored Products
Base metrics
Group by asin
Sponsored Brands
Base metrics
Group by purchasedAsin
Sponsored Display
Base metrics
Group by asin
Sample calls
Sponsored Products
Sponsored Brands
Purchased product reports
Configurations
Configuration	Sponsored Products	Sponsored Brands	Sponsored Display
reportTypeId	spPurchasedProduct	sbPurchasedProduct	sdPurchasedProduct
Maximum date range	31 days	731 days	31 days
Data retention	95 days	731 days	65 days
timeUnit	SUMMARY or DAILY	SUMMARY or DAILY	SUMMARY or DAILY
groupBy	asin	purchasedAsin	asin
format	GZIP_JSON	GZIP_JSON	GZIP_JSON
Sponsored Products
Sponsored Products purchased product reports contain performance data for products that were purchased, but were not advertised as part of a campaign. The purchased product report contains both targeting expressions and keyword IDs. After you have received your report, you can filter on keywordType to distinguish between targeting expressions and keywords.

Base metrics
date, startDate, endDate, addToList, addToListFromClicks, qualifiedBorrows, qualifiedBorrowsFromClicks, royaltyQualifiedBorrows, royaltyQualifiedBorrowsFromClicks, portfolioId, campaignName, campaignId, adGroupName, adGroupId, keywordId, keyword, keywordType, advertisedAsin, purchasedAsin, advertisedSku, campaignBudgetCurrencyCode, matchType, unitsSoldClicks1d, unitsSoldClicks7d, unitsSoldClicks14d, unitsSoldClicks30d, sales1d, sales7d, sales14d, sales30d, purchases1d, purchases7d, purchases14d, purchases30d, unitsSoldOtherSku1d, unitsSoldOtherSku7d, unitsSoldOtherSku14d, unitsSoldOtherSku30d, salesOtherSku1d, salesOtherSku7d, salesOtherSku14d, salesOtherSku30d, purchasesOtherSku1d, purchasesOtherSku7d, purchasesOtherSku14d, purchasesOtherSku30d, kindleEditionNormalizedPagesRead14d, kindleEditionNormalizedPagesRoyalties14d

Group by asin
Additional metrics: N/A

Filters: N/A

Sponsored Brands
Sponsored Brands purchased product reports contain performance data for products that were purchased as a result of your campaign.

Base metrics
campaignId, adGroupId, date, startDate, endDate, campaignBudgetCurrencyCode, campaignName, campaignPriceTypeCode, adGroupName, attributionType, purchasedAsin, ordersClicks14d, productName, productCategory, sales14d, salesClicks14d, orders14d, unitsSold14d, newToBrandSales14d, newToBrandPurchases14d, newToBrandUnitsSold14d, newToBrandSalesPercentage14d, newToBrandPurchasesPercentage14d, newToBrandUnitsSoldPercentage14d, unitsSoldClicks14d, kindleEditionNormalizedPagesRead14d, kindleEditionNormalizedPagesRoyalties14d

Group by purchasedAsin
Additional metrics: N/A

Filters: N/A

Sponsored Display
Base metrics
adGroupId, adGroupName, asinBrandHalo, addToList, addToListFromClicks, qualifiedBorrowsFromClicks, royaltyQualifiedBorrowsFromClicks,addToListFromViews, qualifiedBorrows, qualifiedBorrowsFromViews, royaltyQualifiedBorrows, royaltyQualifiedBorrowsFromViews, campaignBudgetCurrencyCode, campaignId, campaignName, conversionsBrandHalo, conversionsBrandHaloClicks, date, endDate, kindleEditionNormalizedPagesRead, kindleEditionNormalizedPagesReadFromClicks, kindleEditionNormalizedPagesReadFromViews, kindleEditionNormalizedPagesRoyalties, kindleEditionNormalizedPagesRoyaltiesFromClicks, kindleEditionNormalizedPagesRoyaltiesFromViews, promotedAsin, promotedSku, salesBrandHalo, salesBrandHaloClicks, startDate, unitsSoldBrandHalo, unitsSoldBrandHaloClicks

Group by asin
Additional metrics: N/A

Filters: N/A

Sample calls
Sponsored Products
curl --location --request POST 'https://advertising-api.amazon.com/reporting/reports' \
--header 'Content-Type: application/vnd.createasyncreportrequest.v3+json' \
--header 'Amazon-Advertising-API-ClientId: amzn1.application-oa2-client.xxxxxxx' \
--header 'Amazon-Advertising-API-Scope: xxxxxxxx' \
--header 'Authorization: Bearer Atza|xxxxxxxxxx' \
--data-raw '{
    "name":"SP purchased product report 7/5-7/10",
    "startDate":"2022-07-05",
    "endDate":"2022-07-10",
    "configuration":{
        "adProduct":"SPONSORED_PRODUCTS",
        "groupBy":["asin"],
        "columns":["purchasedAsin","advertisedAsin","adGroupName","campaignName","sales14d","campaignId","adGroupId","keywordId","keywordType","keyword"],
        "reportTypeId":"spPurchasedProduct",
        "timeUnit":"SUMMARY",
        "format":"GZIP_JSON"
    }
}'
Sponsored Brands
curl --location --request POST 'https://advertising-api.amazon.com/reporting/reports' \
--header 'Content-Type: application/vnd.createasyncreportrequest.v3+json' \
--header 'Amazon-Advertising-API-ClientId: amzn1.application-oa2-client.xxxxxxx' \
--header 'Amazon-Advertising-API-Scope: xxxxxxxx' \
--header 'Authorization: Bearer Atza|xxxxxxxxxx' \
--data-raw '{
    "name":"SB purchased product report 7/5-7/10",
    "startDate":"2022-07-05",
    "endDate":"2022-07-10",
    "configuration":{
        "adProduct":"SPONSORED_BRANDS",
        "groupBy":["purchasedAsin"],
        "columns":["purchasedAsin","attributionType","adGroupName","campaignName","sales14d","startDate","endDate"],
        "reportTypeId":"sbPurchasedProduct",
        "timeUnit":"SUMMARY",
        "format":"GZIP_JSON"
    }
}'

In this document

Configurations
Base metrics
Group by campaign
Sample call
Gross and invalid traffic reports
Gross and invalid traffic report provides Sponsored Products, Sponsored Brands and Sponsored Display advertisers transparency into the nature of traffic on their campaigns. This report include all campaigns of the requested ad type and provides transparency on gross and invalid traffic metrics at campaign level for the requested days. For example, a Sponsored Products gross and invalid traffic report returns gross and invalid traffic metrics for all Sponsored Products campaigns that received impressions on the chosen dates.

Configurations
Configuration	Sponsored Products	Sponsored Brands	Sponsored Display
reportTypeId	spGrossAndInvalids	sbGrossAndInvalids	sdGrossAndInvalids
Maximum date range	365 days	365 days	365 days
Data retention	365 days	365 days	365 days
timeUnit	SUMMARY or DAILY	SUMMARY or DAILY	SUMMARY or DAILY
groupBy	campaign	campaign	campaign
format	GZIP_JSON or CSV	GZIP_JSON or CSV	GZIP_JSON or CSV
Sponsored Products, Sponsored Brands, and Sponosred Display all support the same columns and configurations for the gross and invalid traffic report.

Base metrics
campaignName, campaignStatus, clicks, date, endDate, grossClickThroughs, grossImpressions, impressions, invalidClickThroughRate, invalidClickThroughs, invalidImpressionRate, invalidImpressions, startDate

Group by campaign
Additional metrics: N/A

Filters:

campaignStatus (values: ENABLED, PAUSED, ARCHIVED)
Sample call
curl --location 'https://advertising-api.amazon.com/reporting/reports' \
--header 'Content-Type: application/vnd.createasyncreportrequest.v3+json' \
--header 'Amazon-Advertising-API-ClientId: amzn1.application-oa2-client.xxxxxxxxxxx' \
--header 'Amazon-Advertising-API-Scope: xxxxxxxx' \
--header 'Authorization: Bearer Atza|xxxxxxxx' \
--data '{
    "name": "SP Gross and Invalid Traffic",
    "startDate": "2023-09-05",
    "endDate": "2023-09-10",
    "configuration": {
        "adProduct": "SPONSORED_PRODUCTS",
        "groupBy": [
            "campaign"
        ],
        "columns": [
            "campaignName",
            "grossImpressions",
            "grossClickThroughs",
            "invalidClickThroughs",
            "invalidClickThroughRate",
            "startDate",
            "endDate"
        ],
        "reportTypeId": "spGrossAndInvalids",
        "timeUnit": "SUMMARY",
        "format": "CSV"
    }
}'

In this document

3PFees
3PPreBidFee
3PPreBidFeeDoubleVerify
3PPreBidFeeIntegralAdScience
3PPreBidFeeOracleDataCloud
3PPreBidFeePixalate
3pFeeAutomotive
3pFeeAutomotiveAbsorbed
3pFeeCPM1
3pFeeCPM1Absorbed
3pFeeCPM2
3pFeeCPM2Absorbed
3pFeeCPM3
3pFeeCPM3Absorbed
3pFeeComScore
3pFeeComScoreAbsorbed
3pFeeDoubleVerify
3pFeeDoubleVerifyAbsorbed
3pFeeDoubleclickCampaignManager
3pFeeDoubleclickCampaignManagerAbsorbed
3pFeeIntegralAdScience
3pFeeIntegralAdScienceAbsorbed
NewToBrandECPP
acosClicks14d
acosClicks7d
adGroupId
adFormat
adGroupName
adId
adKeywordStatus
adProduct
adStatus
addToCart
addToCartBrandHalo
addToCartBrandHaloClicks
addToCartBrandHaloViews
addToCartClicks
addToCartRate
addToCartViews
addToList
addToListBrandHalo
addToListBrandHaloClicks
addToListBrandHaloViews
addToListClicks
addToListFromClicks
addToListFromViews
addToListRate
addToListViews
addToShoppingCart
addToShoppingCartCPA
addToShoppingCartCVR
addToShoppingCartClicks
addToShoppingCartValueAverage
addToShoppingCartValueSum
addToShoppingCartViews
addToWatchlist
addToWatchlistClicks
addToWatchlistRate
addToWatchlistViews
advertisedAsin
advertisedSku
advertiserCountry
advertiserId
advertiserName
advertiserTimezone
agencyFee
alexaSkillEnable
alexaSkillEnableClicks
alexaSkillEnableRate
alexaSkillEnableViews
amazonDSPAudienceFee
amazonDspAudioFrequency
amazonDSPConsoleFee
amazonDspDisplayFrequency
amazonDspOnlineVideoFrequency
amazonDspStreamingTvFrequency
amazonExclusiveReachRate
appStoreFirstOpens
appStoreFirstOpensClicks
appStoreFirstOpensRate
appStoreFirstOpensViews
appStoreFirstSessionHours
appStoreFirstSessionHoursClicks
appStoreFirstSessionHoursViews
appStoreOpens
appStoreOpensClicks
appStoreOpensRate
appStoreOpensViews
appStoreUsageHours
appStoreUsageHoursClicks
appStoreUsageHoursViews
appSubscriptionCost
appSubscriptionFreeTrialCost
appSubscriptionSignUp
appSubscriptionSignUpClicks
appSubscriptionSignUpFreeTrial
appSubscriptionSignUpFreeTrialClicks
appSubscriptionSignUpFreeTrialRate
appSubscriptionSignUpFreeTrialViews
appSubscriptionSignUpPaid
appSubscriptionSignUpPaidClicks
appSubscriptionSignUpPaidCost
appSubscriptionSignUpPaidRate
appSubscriptionSignUpPaidViews
appSubscriptionSignUpRate
appSubscriptionSignUpViews
application
applicationCPA
applicationCVR
applicationClicks
applicationValueAverage
applicationValueSum
applicationViews
asin
asinBrandHalo
attributedSalesSameSku14d
attributedSalesSameSku1d
attributedSalesSameSku30d
attributedSalesSameSku7d
attributionType
audioAdCompanionBannerClicks
audioAdCompanionBannerViews
audioAdCompletionRate
audioAdCompletions
audioAdFirstQuartile
audioAdMidpoint
audioAdMute
audioAdPause
audioAdProgression
audioAdResume
audioAdRewind
audioAdSkip
audioAdStart
audioAdThirdQuartile
audioAdUnmute
audioAdViews
averageCostPerClickToApply
averageCostPerKindleDetailPageView
bidAdjustment
bidAdjustmentRule
bidAdjustmentRuleId
bidAdjustmentRuleVersionId
bidAdjustmentMatchedTerms
bidAdjustmentMatchedTermIds
bidOptimization
bids
brand
brandName
brandSearchRate
brandSearches
brandSearchesClicks
brandSearchesViews
brandedSearchRate
brandedSearches
brandedSearchesClicks
brandedSearchesViews
browseCategory
browserName
browserVersion
campaignApplicableBudgetRuleId
campaignApplicableBudgetRuleName
campaignBiddingStrategy
campaignBudgetAmount
campaignBudgetCurrencyCode
campaignBudgetType
campaignCountry
campaignGoal
campaignId
campaignName
campaignPriceTypeCode
campaignRuleBasedBudgetAmount
campaignStatus
checkout
checkoutCPA
checkoutCVR
checkoutClicks
checkoutValueAverage
checkoutValueSum
checkoutViews
city
clicks
clickThroughRate
clickToApply
clickToApplyBrandHalo
clickToApplyBrandHaloClicks
clickToApplyBrandHaloViews
clickToApplyClicks
clickToApplyConversionRate
clickToApplyViews
combinedECPP
combinedERPM
combinedProductSales
combinedPurchaseRate
combinedPurchases
combinedPurchasesClicks
combinedPurchasesViews
combinedROAS
combinedUnitsSold
completionRateVideoAd
completionRateVideoAdP25
completionRateVideoAdP50
completionRateVideoAdP75
contact
contactCPA
contactCVR
contactClicks
contactValueAverage
contactValueSum
contactViews
contentCategory
contentGenre
contentRating
contentTitle
contentType
conversionType
conversionsBrandHalo
conversionsBrandHaloClicks
cost
costPerClick
costPerCompletedViewVideoAd
costPerCompletedViewVideoAdP25
costPerCompletedViewVideoAdP50
costPerCompletedViewVideoAdP75
costPerNewToBrandPurchase
costPerNewToBrandPurchaseP25
costPerNewToBrandPurchaseP50
costPerNewToBrandPurchaseP75
costPerThousandImpressions
costType
country
cpc
cpcP25
cpcP50
cpcP75
cpm
cpmP25
cpmP50
cpmP75
creativeAdId
creativeExtensionId
creativeExtensionType
creativeId
creativeLanguage
creativeName
creativeSize
creativeType
creativeweight
ctr
ctrP25
ctrP50
ctrP75
cumulativeReach
date
deal
dealId
dealType
detailPageViewBrandHalo
detailPageViewBrandHaloClicks
detailPageViewBrandHaloViews
detailPageViewClicks
detailPageViewRate
detailPageViewRatePromotedClicks
detailPageViewViews
detailPageViews
detailPageViewsClicks
dmaName
downloadedVideoPlayRate
downloadedVideoPlays
downloadedVideoPlaysClicks
downloadedVideoPlaysViews
eCPAddToCart
eCPAddToList
eCPAddToWatchlist
eCPAlexaSkillEnable
eCPAppStoreFirstOpens
eCPAppStoreOpens
eCPAudioAdCompletion
eCPBrandSearch
eCPC
eCPDetailPageView
eCPDownloadedVideoPlays
eCPFreeTrialSubscriptionSignup
eCPM
eCPP
eCPPaidSubscriptionSignup
eCPPlayTrailer
eCPProductReviewPageVisit
eCPRental
eCPSkillInvocation
eCPSubscriptionSignup
eCPVideoAdCompletion
eCPVideoDownload
eCPVideoStream
eCPnewSubscribeAndSave
eRPM
effectiveCostPerDetailPageViewPromotedClicks
effectiveCostPerPurchasePromotedClicks
effectiveCostPerSkillInvocation
einkDetailPageView
einkDetailPageViewBrandHalo
einkDetailPageViewBrandHaloClicks
einkDetailPageViewBrandHaloViews
einkDetailPageViewClicks
einkDetailPageViewViews
endDate
entityId
environmentName
exclusiveReachRate
featuredAsin
flightBudget
flightEndDate
flightId
flightName
flightStartDate
freeTrialSubscriptionSignupClicks
freeTrialSubscriptionSignupRate
freeTrialSubscriptionSignupViews
freeTrialSubscriptionSignups
frequencyAverage
frequencyGroupId
frequencyGroupName
grossClickThroughs
grossImpressions
householdFrequencyAverage
householdReach
impressionFrequencyAverage
impressions
impressionsFrequencyAverage
impressionsViews
incrementalReachRate
interactiveImpressions
intervalEnd
intervalStart
invalidClickThroughRate
invalidClickThroughs
invalidImpressionRate
invalidImpressions
inventoryTier
keyword
keywordBid
keywordId
keywordText
keywordType
kindleDetailPageView
kindleDetailPageViewClicks
kindleDetailPageViewRate
kindleDetailPageViewViews
kindleEditionNormalizedPagesRead
kindleEditionNormalizedPagesReadFromClicks
kindleEditionNormalizedPagesReadFromViews
kindleEditionNormalizedPagesRead14d
kindleEditionNormalizedPagesRoyalties
kindleEditionNormalizedPagesRoyaltiesFromClicks
kindleEditionNormalizedPagesRoyaltiesFromViews
kindleEditionNormalizedPagesRoyalties14d
lead
leadCPA
leadCVR
leadClicks
leadValueAverage
leadValueSum
leadViews
lineItemApprovalStatus
lineItemBudget
lineItemBudgetCap
lineItemComment
lineItemComments
lineItemDeliveryRate
lineItemEndDate
lineItemExternalId
lineItemId
lineItemLanguageTargeting
lineItemName
lineItemStartDate
lineItemStatus
lineItemType
linkOuts
longTermSales
longTermROAS
marketplace
masterClicks
masterImpressions
matchRate
matchType
matchedTargetAsin
measurableImpressions
measurableRate
mobileAppFirstStartAverage
mobileAppFirstStartCPA
mobileAppFirstStartCVR
mobileAppFirstStartClicks
mobileAppFirstStartSum
mobileAppFirstStartViews
mobileAppFirstStarts
newSubscribeAndSave
newSubscribeAndSaveBrandHalo
newSubscribeAndSaveBrandHaloClicks
newSubscribeAndSaveBrandHaloViews
newSubscribeAndSaveClicks
newSubscribeAndSaveRate
newSubscribeAndSaveViews
newToBrandDetailPageViewClicks
newToBrandDetailPageViewRate
newToBrandDetailPageViewViews
newToBrandDetailPageViews
newToBrandDetailPageViewsClicks
newToBrandECPDetailPageView
brandStorePageView
newToBrandERPM
newToBrandProductSales
newToBrandPurchasePercentageBrandHalo
newToBrandPurchaseRate
newToBrandPurchaseRateP25
newToBrandPurchaseRateP50
newToBrandPurchaseRateP75
newToBrandPurchases
newToBrandPurchases14d
newToBrandPurchasesBrandHalo
newToBrandPurchasesBrandHaloClicks
newToBrandPurchasesBrandHaloViews
newToBrandPurchasesClicks
newToBrandPurchasesPercentage
newToBrandPurchasesPercentage14d
newToBrandPurchasesRate
newToBrandPurchasesViews
newToBrandROAS
newToBrandSales
newToBrandSales14d
newToBrandSalesClicks
newToBrandSalesPercentage
newToBrandSalesPercentage14d
newToBrandSalesViews
newToBrandUnitsSold
newToBrandUnitsSold14d
newToBrandUnitsSoldBrandHalo
newToBrandUnitsSoldClicks
newToBrandUnitsSoldPercentage
newToBrandUnitsSoldPercentage14d
notificationClicks
notificationOpens
offAmazonCPA
offAmazonCVR
offAmazonClicks
offAmazonConversions
offAmazonECPP
offAmazonERPM
offAmazonProductSales
offAmazonPurchaseRate
offAmazonPurchases
offAmazonPurchasesClicks
offAmazonPurchasesViews
offAmazonROAS
offAmazonUnitsSold
offAmazonViews
omnichannelMetricsFee
omsLineItemId
omsProposalId
onTargetCostPerImpression
onTargetCPM
onTargetImpressionCost
onTargetImpressions
operatingSystemName
orderBudget
orderCurrency
orderEndDate
orderExternalId
orderId
orderName
orderStartDate
orders14d
ordersClicks14d
other
otherCPA
otherCVR
otherClicks
otherValueAverage
otherValueSum
otherViews
pageViewCPA
pageViewCVR
pageViewClicks
pageViewValueAverage
pageViewValueSum
pageViewViews
pageViews
paidSubscriptionSignupClicks
paidSubscriptionSignupRate
paidSubscriptionSignupViews
paidSubscriptionSignups
parentAsin
peerSetSize
percentOfPurchasesNewToBrand
percentOfPurchasesNewToBrandP25
percentOfPurchasesNewToBrandP50
percentOfPurchasesNewToBrandP75
placement
placementClassification
placementSize
playTrailerRate
playTrailers
playTrailersClicks
playTrailersViews
portfolioId
postalCode
productCategory
productGroup
productName
productReviewPageViewBrandHalo
productReviewPageViewBrandHaloClicks
productReviewPageViewBrandHaloViews
productReviewPageVisitRate
productReviewPageVisits
productReviewPageVisitsClicks
productReviewPageVisitsViews
productSubCategory
promptText
promotedAsin
promotedSku
proposalId
purchaseRate
purchasedAsin
purchases
purchases14d
purchases1d
purchases30d
purchases7d
purchasesBrandHalo
purchasesBrandHaloClicks
purchasesBrandHaloViews
purchasesClicks
purchasesClicksRate
purchasesOtherSku14d
purchasesOtherSku1d
purchasesOtherSku30d
purchasesOtherSku7d
purchasesPromoted
purchasesPromotedClicks
purchasesSameSku14d
purchasesSameSku1d
purchasesSameSku30d
purchasesSameSku7d
purchasesViews
qualifiedBorrows
qualifiedBorrowsFromClicks
qualifiedBorrowsFromViews
reach
region
rentalRate
rentals
rentalsClicks
rentalsViews
reportGranularity
roas
roasClicks14d
roasClicks7d
royaltyQualifiedBorrows
royaltyQualifiedBorrowsFromClicks
royaltyQualifiedBorrowsFromViews
sales
sales14d
sales1d
sales30d
sales7d
salesBrandHalo
salesBrandHaloClicks
newToBrandSalesBrandHalo
salesClicks
salesClicks14d
salesCurrencyCode
salesOtherSku14d
salesOtherSku1d
salesOtherSku30d
salesOtherSku7d
salesPromoted
salesPromotedClicks
salesViews
search
searchCPA
searchCVR
searchClicks
searchTerm
searchValueAverage
searchValueSum
searchViews
segmentClassCode
segmentId
segmentMarketplaceId
segmentName
segmentSource
segmentType
signUp
signUpCPA
signUpCVR
signUpClicks
signUpValueAverage
signUpValueSum
signUpViews
simplifiedPath
site
skillInvocation
skillInvocationClicks
skillInvocationRate
skillInvocationViews
spend
sponsoredBrandsDisplayFrequency
sponsoredBrandsVideoFrequency
sponsoredDisplayDisplayFrequency
sponsoredDisplayFrequency
sponsoredDisplayOnlineVideoFrequency
sponsoredProductsFrequency
sponsoredTvStreamingTvFrequency
startDate
subscribe
subscribeCPA
subscribeCVR
subscribeClicks
subscribeValueAverage
subscribeValueSum
subscribeViews
subscriptionSignupClicks
subscriptionSignupRate
subscriptionSignupViews
subscriptionSignups
supplyCost
supplySource
supplySourceId
targetDemographic
targeting
targetingExpression
targetingId
targetingMethod
targetingText
targetingType
topOfSearchImpressionShare
totalAddToCart
totalAddToCartClicks
totalAddToCartRate
totalAddToCartViews
totalAddToList
totalAddToListClicks
totalAddToListRate
totalAddToListViews
totalCost
totalDetailPageView
totalDetailPageViewClicks
totalDetailPageViewRate
totalDetailPageViewViews
totalECPAddToCart
totalECPAddToList
totalECPDetailPageView
totalECPP
totalECPProductReviewPageVisit
totalECPSubscribeAndSave
totalERPM
totalFee
totalNewToBrandDPVClicks
totalNewToBrandDPVRate
totalNewToBrandDPVViews
totalNewToBrandDPVs
totalNewToBrandECPDetailPageView
totalNewToBrandECPP
totalNewToBrandERPM
totalNewToBrandPurchaseRate
totalNewToBrandPurchases
totalNewToBrandPurchasesClicks
totalNewToBrandPurchasesPercentage
totalNewToBrandPurchasesViews
totalNewToBrandROAS
totalNewToBrandSales
totalNewToBrandUnitsSold
totalProductReviewPageVisitRate
totalProductReviewPageVisits
totalProductReviewPageVisitsClicks
totalProductReviewPageVisitsViews
totalPurchaseRate
totalPurchases
totalPurchasesClicks
totalPurchasesViews
totalROAS
totalSales
totalSubscribeAndSave
totalSubscribeAndSaveClicks
totalSubscribeAndSaveRate
totalSubscribeAndSaveViews
totalUnitsSold
unitsSold
unitsSold14d
unitsSoldBrandHalo
unitsSoldBrandHaloClicks
unitsSoldClicks
unitsSoldClicks14d
unitsSoldClicks1d
unitsSoldClicks30d
unitsSoldClicks7d
unitsSoldOtherSku14d
unitsSoldOtherSku1d
unitsSoldOtherSku30d
unitsSoldOtherSku7d
unitsSoldPromotedClicks
unitsSoldSameSku14d
unitsSoldSameSku1d
unitsSoldSameSku30d
unitsSoldSameSku7d
unitsSoldViews
video5SecondViewRate
video5SecondViews
videoAdClicks
videoAdComplete
videoAdCompletionRate
videoAdCreativeViews
videoAdEndStateClicks
videoAdFirstQuartile
videoAdImpressions
videoAdMidpoint
videoAdMute
videoAdPause
videoAdReplays
videoAdResume
videoAdSkipBacks
videoAdSkipForwards
videoAdStart
videoAdThirdQuartile
videoAdUnmute
videoCompleteViews
videoDownloadRate
videoDownloads
videoDownloadsClicks
videoDownloadsViews
videoFirstQuartileViews
videoMidpointViews
videoStreams
videoStreamsClicks
videoStreamsRate
videoStreamsViews
videoThirdQuartileViews
videoUnmutes
viewClickThroughRate
viewabilityRate
viewableImpressions
winRate
Metrics
All metrics available for the version 3 reporting API.

3PFees
Type: Decimal

Description: The total CPM charges applied for using 3P data providers.

Report types: dspCampaign, dspInventory

3PPreBidFee
Type: Decimal

Description: Total cost for using third-party pre-bid targeting.

Report types: dspCampaign

3PPreBidFeeDoubleVerify
Type: Decimal

Description: The third party pre-bid fee applied for using DoubleVerify.

Report types: dspCampaign

3PPreBidFeeIntegralAdScience
Type: Decimal

Description: The third party pre-bid fee applied for using IntegralAdScience.

Report types: dspCampaign

3PPreBidFeeOracleDataCloud
Type: Decimal

Description: The third party pre-bid fee applied for using OracleDataCloud.

Report types: dspCampaign

3PPreBidFeePixalate
Type: Decimal

Description: The third party pre-bid fee applied for using Pixalate.

Report types: dspCampaign

3pFeeAutomotive
Type: Decimal

Description: A third-party fee applied to automotive data.

Report types: dspCampaign, dspInventory

3pFeeAutomotiveAbsorbed
Type: Decimal

Description: CPM charge applied to impressions to track Automotive segment fees. The cost is itemized in reports, but absorbed by the user and excluded from total costs.

Report types: dspCampaign, dspInventory

3pFeeCPM1
Type: Decimal

Description: A third-party fee applied.

Report types: dspCampaign, dspInventory

3pFeeCPM1Absorbed
Type: Decimal

Description: CPM charge applied to impressions to track general 3P technology fees. The cost is itemized in reports, but absorbed by the user and excluded from total costs.

Report types: dspCampaign, dspInventory

3pFeeCPM2
Type: Decimal

Description: A third-party fee applied.

Report types: dspCampaign, dspInventory

3pFeeCPM2Absorbed
Type: Decimal

Description: CPM charge applied to impressions to track general 3P technology fees. The cost is itemized in reports, but absorbed by the user and excluded from total costs.

Report types: dspCampaign, dspInventory

3pFeeCPM3
Type: Decimal

Description: A third-party fee applied.

Report types: dspCampaign, dspInventory

3pFeeCPM3Absorbed
Type: Decimal

Description: CPM charge applied to impressions to track general 3P technology fees. The cost is itemized in reports, but absorbed by the user and excluded from total costs.

Report types: dspCampaign, dspInventory

3pFeeComScore
Type: Decimal

Description: The third-party fee applied for using ComScore.

Report types: dspCampaign, dspInventory

3pFeeComScoreAbsorbed
Type: Decimal

Description: CPM charge applied to impressions to track ComScore technology fees. The cost is itemized in reports, but absorbed by the user and excluded from total costs.

Report types: dspCampaign, dspInventory

3pFeeDoubleVerify
Type: Decimal

Description: The third-party fee applied for using DoubleVerify.

Report types: dspCampaign, dspInventory

3pFeeDoubleVerifyAbsorbed
Type: Decimal

Description: CPM charge applied to impressions to track DoubleVerify technology fees. The cost is itemized in reports, but absorbed by the user and excluded from total costs.

Report types: dspCampaign, dspInventory

3pFeeDoubleclickCampaignManager
Type: Decimal

Description: The third-party fee applied for using DoubleClick Campaign Manager.

Report types: dspCampaign, dspInventory

3pFeeDoubleclickCampaignManagerAbsorbed
Type: Decimal

Description: CPM charge applied to impressions to track Doubleclick Campaign Manager technology fees. The cost is itemized in reports, but absorbed by the user and excluded from total costs.

Report types: dspCampaign, dspInventory

3pFeeIntegralAdScience
Type: Decimal

Description: The third-party fee applied for using Integral Ad Science.

Report types: dspCampaign, dspInventory

3pFeeIntegralAdScienceAbsorbed
Type: Decimal

Description: CPM charge applied to impressions to track Integral Ad Science technology fees. The cost is itemized in reports, but absorbed by the user and excluded from total costs.

Report types: dspCampaign, dspInventory

NewToBrandECPP
Type: Decimal

Description: Effective (average) cost to acquire a new-to-brand purchase conversion for a promoted product. (New-to-brand eCPP = Total cost / New-to-brand purchases) Use Total new-to-brand eCPP to see all conversions for the brands' products.

Report types: dspCampaign, dspInventory, dspAudience

acosClicks14d
Type: Decimal

Description: Advertising cost of sales based on purchases made within 14 days of an ad click.

Report types: spTargeting, spSearchTerm, spAdvertisedProduct, spPromptAdExtension

acosClicks7d
Type: Decimal

Description: Advertising cost of sales based on purchases made within 7 days of an ad click.

Report types: spTargeting, spSearchTerm, spAdvertisedProduct, spPromptAdExtension

adGroupId
Type: Integer

Description: Unique numerical ID of the ad group.

Report types: spCampaigns, sbAdGroups, spTargeting, sbTargeting, spSearchTerm, sbSearchTerm, spPurchasedProduct, sbPurchasedProduct, sdAdGroups, sdTargeting, sdAdvertisedProduct, sdPurchasedProduct, stCampaigns, stTargeting, sbAds, spAdvertisedProduct, spPromptAdExtension

adFormat
Type: String

Description: The format of the ad like video, image, etc.

Report types: benchmarks

adGroupName
Type: String

Description: The name of the ad group as entered by the advertiser.

Report types: spCampaigns, sbAdGroups, spTargeting, sbTargeting, spSearchTerm, sbSearchTerm, spPurchasedProduct, sbPurchasedProduct, sdAdGroups, sdTargeting, sdAdvertisedProduct, sdPurchasedProduct, stCampaigns, stTargeting, sbAds, spAdvertisedProduct, spPromptAdExtension

adId
Type: Integer

Description: Unique numerical ID of the ad.

Report types: sdAdvertisedProduct, sbAds, spAdvertisedProduct, spPromptAdExtension

adKeywordStatus
Type: String

Description: Current status of a keyword.

Report types: spTargeting, sbTargeting, spSearchTerm, sbSearchTerm, sdTargeting, stTargeting

adProduct
Type: String

Description: Amazon ad product.

Report types: benchmarks

adStatus
Type: String

Description: Status of the ad group.

Report types: spCampaigns, sbAdGroups, stCampaigns, stTargeting

addToCart
Type: Integer

Description: Number of times shoppers added a brand's products to their cart, attributed to an ad view or click.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, stCampaigns, stTargeting, sbAds, dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

addToCartBrandHalo
Type: Integer

Description: Number of times shoppers added a brand halo product to their cart, attributed to an ad view or click. Use Total ATC to see all conversions for the brands' products.

Report types: dspProduct

addToCartBrandHaloClicks
Type: Integer

Description: Number of times shoppers added a brand halo product to their cart, attributed to an ad click. Use Total ATC clicks to see all conversions for the brands' products.

Report types: dspProduct

addToCartBrandHaloViews
Type: Integer

Description: Number of times shoppers added a brand halo product to their cart, attributed to an ad view. Use Total ATC views to see all conversions for the brands' products.

Report types: dspProduct

addToCartClicks
Type: Integer

Description: Number of times shoppers added a brand's products to their cart, attributed to an ad click.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, stCampaigns, stTargeting, sbAds, dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

addToCartRate
Type: Decimal

Description: Calculated by divididing addToCart by impressions.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, sbAds, dspCampaign, dspInventory, dspAudience

addToCartViews
Type: Integer

Description: Number of times shoppers added the brands' products to their cart, attributed to an ad view.

Report types: sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, stCampaigns, stTargeting, dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

addToList
Type: Integer

Description: Number of times shoppers added a promoted product to a wish list, gift list, or registry, attributed to an ad view or click. Use Total ATL to see all conversions for the brands' products.

Report types: spCampaigns, sbCampaigns, sbAdGroups, sbPlacement, spTargeting, sbTargeting, spSearchTerm, sbSearchTerm, spPurchasedProduct, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, sdPurchasedProduct, sbAds, spAdvertisedProduct, dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

addToListBrandHalo
Type: Integer

Description: Number of times shoppers added a brand halo product to a wish list, gift list, or registry, attributed to an ad view or click. Use Total ATL to see all conversions for the brands' products.

Report types: dspProduct

addToListBrandHaloClicks
Type: Integer

Description: Number of times shoppers added a brand halo product to a wish list, gift list, or registry, attributed to an ad click. Use Total ATL clicks to see all conversions for the brands' products.

Report types: dspProduct

addToListBrandHaloViews
Type: Integer

Description: Number of times shoppers added a brand halo product to a wish list, gift list, or registry, attributed to an ad view. Use Total ATL views to see all conversions for the brands' products.

Report types: dspProduct

addToListClicks
Type: Integer

Description: Number of times shoppers added a promoted product to a wish list, gift list, or registry, attributed to an ad click. Use Total ATL clicks to see all conversions for the brands' products.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

addToListFromClicks
Type: Integer

Description: Number of times shoppers added a promoted product to a wish list, gift list, or registry, attributed to an ad click.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sbSearchTerm, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, sdPurchasedProduct, sbAds

addToListFromViews
Type: Integer

Description: Number of times shoppers added a promoted product to a wish list, gift list, or registry, attributed to an ad view.

Report types: sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, sdPurchasedProduct

addToListRate
Type: Integer

Description: Rate of Add to List conversions for promoted products relative to the number of impressions. (ATLR = ATL / Impressions) Use Total ATLR to see all conversions for the brands' products.

Report types: dspCampaign, dspInventory, dspAudience

addToListViews
Type: Decimal

Description: Number of times shoppers added a promoted product to a wish list, gift list, or registry, attributed to an ad view. Use Total ATL views to see all conversions for the brands' products.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

addToShoppingCart
Type: Integer

Description: The number of Add to shopping cart conversions.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

addToShoppingCartCPA
Type: Decimal

Description: The average cost to acquire an Add to shopping cart conversion. (ATSC CPA = Total cost / ATSC)

Report types: dspCampaign, dspInventory, dspAudience

addToShoppingCartCVR
Type: Decimal

Description: The number of Add to shopping cart conversions relative to the number of ad impressions. (ATSC CVR = ATSC / Impressions)

Report types: dspCampaign, dspInventory, dspAudience

addToShoppingCartClicks
Type: Integer

Description: The number of Add to shopping cart conversions attributed to an ad click.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

addToShoppingCartValueAverage
Type: Decimal

Description: Average value associated with an Add to Shopping cart conversion. (ATSC value average = ATSC value sum / ATSC)

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

addToShoppingCartValueSum
Type: Decimal

Description: Sum of Add to shopping cart conversion values

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

addToShoppingCartViews
Type: Integer

Description: The number of Add to shopping cart conversions attributed to an ad view.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

addToWatchlist
Type: Integer

Description: The number of times Add to Watchlist was clicked on a featured product.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

addToWatchlistClicks
Type: Integer

Description: The number of Add to Watchlist clicks attributed to ad click-throughs.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

addToWatchlistRate
Type: Decimal

Description: The number of Add to Watchlist clicks relative to the number of impressions. (ATWR = ATW / Impressions)

Report types: dspCampaign, dspInventory, dspAudience

addToWatchlistViews
Type: Integer

Description: The number of Add to Watchlist clicks attributed to ad impressions.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

advertisedAsin
Type: String

Description: The ASIN or retailer offer ID associated to an advertised product. This value may differ in format and length from a standard 10-character ASIN.

Report types: spPurchasedProduct, spAdvertisedProduct, spPromptAdExtension

advertisedSku
Type: String

Description: The SKU being advertised. Not available for vendors.

Report types: spPurchasedProduct, spAdvertisedProduct, spPromptAdExtension

advertiserCountry
Type: String

Description: The country assigned to the advertiser.

Report types: dspCampaign, dspInventory, dspAudience

advertiserId
Type: String

Description: The unique identifier for the advertiser.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience, dspAudioAndVideo, dspReachFrequency, dspBidAdjustment, benchmarks

advertiserName
Type: String

Description: The customer that has an advertising relationship with Amazon.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience, dspAudioAndVideo, dspReachFrequency, dspBidAdjustment, benchmarks

advertiserTimezone
Type: String

Description: The time zone the advertiser uses for reporting and ad serving purposes.

Report types: dspCampaign, dspInventory, dspAudience

agencyFee
Type: Decimal

Description: A percentage or flat fee removed from the total budget to compensate the agency that is managing the media buy.

Report types: dspCampaign, dspInventory, dspGeo, dspTech

alexaSkillEnable
Type: Integer

Description: The number of Alexa skill enable conversions

Report types: dspCampaign

alexaSkillEnableClicks
Type: Integer

Description: The number of detail page view conversions attributed to ad click-throughs

Report types: dspCampaign

alexaSkillEnableRate
Type: Decimal

Description: The number of Alexa skill enable conversions relative to the number of ad impressions. (Alexa skill enable rate = Alexa skill enable / Impressions)

Report types: dspCampaign

alexaSkillEnableViews
Type: Integer

Description: The number of alexa skill enable conversions attributed to ad impressions views

Report types: dspCampaign

amazonDSPAudienceFee
Type: Decimal

Description: CPM charge applied to impressions that leverage Amazon's behavioral targeting.

Report types: dspCampaign, dspInventory, dspAudience

amazonDspAudioFrequency
Type: Decimal

Description: Average number of Amazon DSP audio occurrences in the simplified path.

Report types: conversionPath

amazonDSPConsoleFee
Type: Decimal

Description: The technology fee applied to the media supply costs.

Report types: dspCampaign, dspInventory, dspAudience

amazonDspDisplayFrequency
Type: Decimal

Description: Average number of Amazon DSP display occurrences in the simplified path.

Report types: conversionPath

amazonDspOnlineVideoFrequency
Type: Decimal

Description: Average number of Amazon DSP online video occurrences in the simplified path.

Report types: conversionPath

amazonDspStreamingTvFrequency
Type: Decimal

Description: Average number of Amazon DSP streaming TV occurrences in the simplified path.

Report types: conversionPath

amazonExclusiveReachRate
Type: Decimal

Description: The percentage of unique viewers reached by a streaming TV inventory that were not reached by any other streaming TV inventory in the campaign. (Amazon exclusive reach rate = 100 X [exclusive reach for streaming TV inventory / total streaming TV reach]).

Report types: dspReachFrequency

appStoreFirstOpens
Type: Integer

Description: The number of first-time app opens attributed to a click or view on an ad

Report types: dspCampaign, dspProduct

appStoreFirstOpensClicks
Type: Integer

Description: The number of first-time app opens attributed to a click on an ad

Report types: dspCampaign, dspProduct

appStoreFirstOpensRate
Type: Decimal

Description: The ratio of how often customers opened the app for the first time when an ad was displayed. This is calculated as first app opens divided by impressions.

Report types: dspCampaign

appStoreFirstOpensViews
Type: Integer

Description: The number of first-time app opens attributed to ad views.

Report types: dspCampaign, dspProduct

appStoreFirstSessionHours
Type: Integer

Description: The number of hours spent using the app during first-time app open sessions attributed to a click or view on ad ad.

Report types: dspCampaign, dspProduct

appStoreFirstSessionHoursClicks
Type: Integer

Description: The number of hours spent using the app during first-time app open sessions attributed to a click on an ad.

Report types: dspCampaign, dspProduct

appStoreFirstSessionHoursViews
Type: Integer

Description: The number of hours spent using the app during first-time app open sessions attributed to ad views.

Report types: dspCampaign, dspProduct

appStoreOpens
Type: Integer

Description: The number of first-time and recurring app opens attributed to a click or view on an ad

Report types: dspCampaign, dspProduct

appStoreOpensClicks
Type: Integer

Description: The number of first-time and recurring app opens attributed to a click on an ad

Report types: dspCampaign, dspProduct

appStoreOpensRate
Type: Decimal

Description: The ratio of app opens to ad impressions. This is calculated as first-time and recurring app opens divided by impressions.

Report types: dspCampaign

appStoreOpensViews
Type: Integer

Description: The number of first-time and recurring app opens attributed to ad views.

Report types: dspCampaign, dspProduct

appStoreUsageHours
Type: Decimal

Description: The number of hours spent using the app during first-time and recurring app open sessions attributed to a click or view on ad ad.

Report types: dspCampaign, dspProduct

appStoreUsageHoursClicks
Type: Decimal

Description: The number of hours spent using the app during first-time and recurring app open sessions attributed to a click on an ad.

Report types: dspCampaign, dspProduct

appStoreUsageHoursViews
Type: Decimal

Description: The number of hours spent using the app during first-time and recurring app open sessions attributed to ad views.

Report types: dspCampaign, dspProduct

appSubscriptionCost
Type: Decimal

Description: The cost to acquire free trial and paid app subscriptions. This is calculated as total cost divided by app subscription sign-ups.

Report types: dspGeo

appSubscriptionFreeTrialCost
Type: Decimal

Description: The cost to acquire free trial app subscriptions. This is calculated as total cost divided by free trial app subscription sign-ups.

Report types: dspGeo

appSubscriptionSignUp
Type: Integer

Description: The number of free trial and paid app subscriptions associated with a click or view on your ad.

Report types: dspProduct, dspGeo

appSubscriptionSignUpClicks
Type: Integer

Description: The number of free trial and paid app subscriptions associated with a click on your ad.

Report types: dspProduct, dspGeo

appSubscriptionSignUpFreeTrial
Type: Integer

Description: The number of free trial app subscriptions associated with a click or view on your ad.

Report types: dspProduct, dspGeo

appSubscriptionSignUpFreeTrialClicks
Type: Integer

Description: The number of free trial app subscriptions associated with a click on your ad.

Report types: dspProduct, dspGeo

appSubscriptionSignUpFreeTrialRate
Type: Decimal

Description: The ratio of how often customers signed up for a free trial subscription when your ad was displayed. This is calculated as free trial app subscription sign-ups divided by impressions.

Report types: dspGeo

appSubscriptionSignUpFreeTrialViews
Type: Integer

Description: The number of free trial app subscriptions associated with ad impressions.

Report types: dspProduct, dspGeo

appSubscriptionSignUpPaid
Type: Integer

Description: The number of paid app subscriptions associated with a click or view on your ad.

Report types: dspProduct, dspGeo

appSubscriptionSignUpPaidClicks
Type: Integer

Description: The number of paid app subscriptions associated with a click on your ad.

Report types: dspProduct, dspGeo

appSubscriptionSignUpPaidCost
Type: Decimal

Description: The cost to acquire paid app subscriptions. This is calculated as total cost divided by paid app subscription sign-ups.

Report types: dspGeo

appSubscriptionSignUpPaidRate
Type: Decimal

Description: The ratio of how often customers signed up for a paid app subscription when your ad was displayed. This is calculated as paid app subscription sign-ups divided by impressions.

Report types: dspGeo

appSubscriptionSignUpPaidViews
Type: Integer

Description: The number of paid app subscriptions associated with ad impressions.

Report types: dspProduct, dspGeo

appSubscriptionSignUpRate
Type: Decimal

Description: The ratio of how often customers signed up for a free trial or paid app subscription when your ad was displayed. This is calculated as app subscription sign-ups divided by impressions.

Report types: dspGeo

appSubscriptionSignUpViews
Type: Integer

Description: The number of free trial and paid app subscriptions associated with ad impressions.

Report types: dspProduct, dspGeo

application
Type: Integer

Description: The number of Application conversions.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

applicationCPA
Type: Decimal

Description: The average cost to acquire an Application conversion. (Application CPA = Total cost / Application)

Report types: dspCampaign, dspInventory, dspAudience

applicationCVR
Type: Decimal

Description: The number of Application conversions relative to the number of ad impressions. (Application CVR = Application / Impressions)

Report types: dspCampaign, dspInventory, dspAudience

applicationClicks
Type: Integer

Description: The number of Application conversions attributed to an ad click.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

applicationValueAverage
Type: Decimal

Description: Average value associated with an Application conversion. (Application value average = Application value sum / Application)

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

applicationValueSum
Type: Decimal

Description: Sum of Application conversion values

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

applicationViews
Type: Integer

Description: The number of Application conversions attributed to an ad view.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

asin
Type: String

Description: A unique block of letters and/or numbers that identify all products sold on Amazon.

Report types: dspProduct

asinBrandHalo
Type: String

Description: Represents a product that was purchased after an ad click but has a different SKU/ASIN that what was advertised.

Report types: sdPurchasedProduct

attributedSalesSameSku14d
Type: Decimal

Description: Total value of sales occurring within 14 days of ad click where the purchased SKU was the same as the SKU advertised. Sponsored Products only.

Report types: spCampaigns, spTargeting, spSearchTerm, spAdvertisedProduct, spGlobalAudiences, spPromptAdExtension

attributedSalesSameSku1d
Type: Decimal

Description: Total value of sales occurring within 1 day of ad click where the purchased SKU was the same as the SKU advertised.

Report types: spCampaigns, spTargeting, spSearchTerm, spAdvertisedProduct, spGlobalAudiences, spPromptAdExtension

attributedSalesSameSku30d
Type: Decimal

Description: Total value of sales occurring within 30 days of ad click where the purchased SKU was the same as the SKU advertised.

Report types: spCampaigns, spTargeting, spSearchTerm, spAdvertisedProduct, spGlobalAudiences, spPromptAdExtension

attributedSalesSameSku7d
Type: Decimal

Description: Total value of sales occurring within 7 days of ad click where the purchased SKU was the same as the SKU advertised.

Report types: spCampaigns, spTargeting, spSearchTerm, spAdvertisedProduct, spGlobalAudiences, spPromptAdExtension

attributionType
Type: String

Description: Describes whether a purchase is attributed to a promoted product or brand-halo effect.

Report types: sbPurchasedProduct

audioAdCompanionBannerClicks
Type: Integer

Description: Tracks the number of times that the audio ad companion banner was clicked.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

audioAdCompanionBannerViews
Type: Integer

Description: Tracks the number of times that the audio ad companion banner was displayed.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

audioAdCompletionRate
Type: Decimal

Description: The number of audio completions relative to the number of audio starts.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

audioAdCompletions
Type: Integer

Description: Tracks the number of times the audio ad plays to the end.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

audioAdFirstQuartile
Type: Integer

Description: Tracks the number of times the audio ad plays to 25% of its length.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

audioAdMidpoint
Type: Integer

Description: Tracks the number of times the audio ad plays to 50% of its length.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

audioAdMute
Type: Integer

Description: Tracks the number of times a user mutes the audio ad.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

audioAdPause
Type: Integer

Description: The number of times a user pauses the audio ad.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

audioAdProgression
Type: Decimal

Description: Tracks an optimal audio ad time marker agreed upon with the publisher

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

audioAdResume
Type: Integer

Description: Tracks the number of times a user resumes playback of the audio ad.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

audioAdRewind
Type: Integer

Description: Tracks the number of times a user rewinds the audio ad.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

audioAdSkip
Type: Integer

Description: Tracks the number of times a user skips the audio ad.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

audioAdStart
Type: Integer

Description: Tracks the number of times audio ad starts playing.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

audioAdThirdQuartile
Type: Integer

Description: Tracks the number of times the audio ad plays to 75% of its length.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

audioAdUnmute
Type: Integer

Description: Tracks the number of times a user skips the audio ad.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

audioAdViews
Type: Integer

Description: Tracks the number of times that some playback of the audio ad has occurred.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

averageCostPerClickToApply
Type: Decimal

Description: The average cost to acquire a Click to apply conversion. (eCPCTA = Total cost / CTA)

Report types: dspAudience

averageCostPerKindleDetailPageView
Type: Decimal

Description: The average cost to acquire an Ad Details page view conversion on a Kindle E Ink device. (eCPDPVK = Total cost / DPVK)

Report types: dspAudience

bidAdjustment
Type: Decimal

Description: The amount the bid will be multiplied by. If a bid request is matched with multiple terms, this is your final bid adjustment from multiplying multiple factors together.

Report types: dspBidAdjustment

bidAdjustmentRule
Type: String

Description: The name of the bid adjustment rule or ruleDescription in API.

Report types: dspBidAdjustment

bidAdjustmentRuleId
Type: String

Description: A unique identifier for the bid adjustment rule.

Report types: dspBidAdjustment

bidAdjustmentRuleVersionId
Type: String

Description: An identifier representing the version of a bid adjustment rule.

Report types: dspBidAdjustment

bidAdjustmentMatchedTerms
Type: String

Description: The list of bid adjustment terms that matched with a bid request.

Report types: dspBidAdjustment

bidAdjustmentMatchedTermIds
Type: String

Description: The list of unique identifiers for the matched bid adjustment terms. [] (empty bracket) indicates default traffic without bid adjustments. The unique identifier for each bid adjustment term is generated by the system, and can be retrieved by downloading the CSV file (1st column) for the uploaded bid adjustments in the console, or using the GetBidModifierRule or ListBidModifierRules APIs.

Report types: dspBidAdjustment

bidOptimization
Type: String

Description: Bid optimization for Sponsored Display ad groups. For vCPM campaigns, the value is always reach. For CPC campaigns, value is either clicks or conversions.

Report types: sdAdGroups, sdAdvertisedProduct

bids
Type:: Integer

Description: Number of bids sent through the Amazon DSP.

Report types: dspBidAdjustment

brand
Type: String

Description: Brand advertising with Amazon Ads.

Report types: benchmarks

brandName
Type: String

Description: The name of the brand the campaign is advertising.

Report types: dspProduct, conversionPath

brandSearchRate
Type: Decimal

Description: The number of branded search conversions relative to the number of ad impressions. (Branded search rate = Branded searches / Impressions)

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

brandSearches
Type: Integer

Description: The number of times shoppers searched for a brand promoted in the campaign, attributed to an ad interaction.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

brandSearchesClicks
Type: Integer

Description: The number of branded search conversions attributed to ad click-throughs.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

brandSearchesViews
Type: Integer

Description: The number of branded search conversions attributed to ad impressions.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

brandedSearchRate
Type: Decimal

Description: Rate of Branded Searches relative to the number of impressions. (BS/Impressions)

Report types: sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct

brandedSearches
Type: Integer

Description: The number of searches that included the name of your brand occurring within 14 days of an ad click or view.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, stCampaigns, stTargeting, sbAds

brandedSearchesClicks
Type: Integer

Description: The number of searches that included the name of your brand occurring within 14 days of an ad click.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, stCampaigns, stTargeting, sbAds

brandedSearchesViews
Type: Integer

Description: The number of times shoppers searched for a brand promoted in the campaign, attributed to an ad view.

Report types: sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, stCampaigns, stTargeting

browseCategory
Type: String

Description: The browse node category associated with the benchmarked brand.

Report types: benchmarks

browserName
Type: String

Description: The web browsers the customers used to view the ad

Report types: dspTech

browserVersion
Type: String

Description: The specific browser versions the customers used to view the ad

Report types: dspTech

campaignApplicableBudgetRuleId
Type: String

Description: The ID associated to the active budget rule for a campaign.

Report types: spCampaigns

campaignApplicableBudgetRuleName
Type: String

Description: The name associated to the active budget rule for a campaign.

Report types: spCampaigns

campaignBiddingStrategy
Type: String

Description: The bidding strategy associated with a campaign.

Report types: spCampaigns

campaignBudgetAmount
Type: Decimal

Description: Total budget allocated to the campaign.

Report types: spCampaigns, sbCampaigns, sbAdGroups, sbPlacement, spTargeting, sbTargeting, spSearchTerm, sbSearchTerm, sdCampaigns, stCampaigns, stTargeting, sbAds, spAdvertisedProduct, spGlobalAudiences, spGlobalAudiences, sbAudiences

campaignBudgetCurrencyCode
Type: String

Description: The currency code associated with the campaign.

Report types: spCampaigns, sbCampaigns, sbAdGroups, sbPlacement, spTargeting, sbTargeting, spSearchTerm, sbSearchTerm, spPurchasedProduct, sbPurchasedProduct, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, sdPurchasedProduct, stCampaigns, stTargeting, sbAds, spAdvertisedProduct

campaignBudgetType
Type: String

Description: One of daily or lifetime.

Report types: spCampaigns, sbCampaigns, sbAdGroups, sbPlacement, spTargeting, sbTargeting, spSearchTerm, sbSearchTerm, stCampaigns, stTargeting, sbAds, spAdvertisedProduct, spGlobalAudiences, sbAudiences

campaignCountry
Type: String

Description: The country in which the campaign is delivering.

Report types: benchmarks

campaignGoal
Type: String

Description: Campaign goal type.

Report types: benchmarks

campaignId
Type: Integer

Description: The ID associated with a campaign.

Report types: spCampaigns, sbCampaigns, sbAdGroups, sbPlacement, spTargeting, sbTargeting, spSearchTerm, sbSearchTerm, spPurchasedProduct, sbPurchasedProduct, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, sdPurchasedProduct, stCampaigns, stTargeting, sbAds, spAdvertisedProduct, spGlobalAudiences, sbAudiences, spPromptAdExtension

campaignName
Type: String

Description: The name associated with a campaign.

Report types: spCampaigns, sbCampaigns, sbAdGroups, sbPlacement, spTargeting, sbTargeting, spSearchTerm, sbSearchTerm, spPurchasedProduct, sbPurchasedProduct, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, sdPurchasedProduct, stCampaigns, stTargeting, spGrossandInvalids, sbGrossandInvalids, sdGrossandInvalids, sbAds, spAdvertisedProduct, spGlobalAudiences, sbAudiences, spPromptAdExtension

campaignPriceTypeCode
Type: String

Description: The code of the campaign cost type.

Report types: sbPurchasedProduct

campaignRuleBasedBudgetAmount
Type: Decimal

Description: The value of the rule-based budget for a campaign.

Report types: spCampaigns

campaignStatus
Type: String

Description: The status of a campaign.

Report types: spCampaigns, sbCampaigns, sbAdGroups, sbPlacement, spTargeting, sbTargeting, spSearchTerm, sbSearchTerm, sdCampaigns, stCampaigns, stTargeting, spGrossandInvalids, sbGrossandInvalids, sdGrossandInvalids, sbAds, spAdvertisedProduct, spGlobalAudiences, sbAudiences

checkout
Type: Integer

Description: The number of Checkout conversions.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

checkoutCPA
Type: Decimal

Description: The average cost to acquire a Checkout conversion. (Checkout CPA = Total cost / Checkout)

Report types: dspCampaign, dspInventory, dspAudience, dspGeo

checkoutCVR
Type: Decimal

Description: The number of Checkout conversions relative to the number of ad impressions. (Checkout CVR = Checkout / Impressions)

Report types: dspCampaign, dspInventory, dspAudience, dspGeo

checkoutClicks
Type: Integer

Description: The number of Checkout conversions attributed to an ad click.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

checkoutValueAverage
Type: Decimal

Description: Average value associated with a Checkout conversion. (Checkout value average = Checkout value sum / Checkout)

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

checkoutValueSum
Type: Decimal

Description: Sum of Checkout conversion values

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

checkoutViews
Type: Integer

Description: The number of Checkout conversions attributed to an ad view.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

city
Type: String

Description: City.

Report types: dspGeo

clicks
Type: Integer

Description: Total number of clicks on an ad.

Report types: spCampaigns, sbCampaigns, sbAdGroups, sbPlacement, spTargeting, sbTargeting, spSearchTerm, sbSearchTerm, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, stCampaigns, stTargeting, spGrossandInvalids, sbGrossandInvalids, sdGrossandInvalids, sbAds, spAdvertisedProduct, dspCampaign, dspInventory, dspTech, dspGeo, dspAudience, spGlobalAudiences, sbAudiences, dspProduct, spPromptAdExtension

clickThroughRate
Type: Decimal

Description: Clicks divided by impressions.

Report types: spCampaigns, spTargeting, spSearchTerm, stCampaigns, stTargeting, spAdvertisedProduct, dspCampaign, dspInventory, dspTech, dspGeo, dspAudience, spGlobalAudiences, sbAudiences, spPromptAdExtension

clickToApply
Type: Integer

Description: The number of time Click to apply was clicked for a featured product.

Report types: dspProduct, dspTech, dspGeo, dspAudience

clickToApplyBrandHalo
Type: Integer

Description: The number of times Click to apply was clicked on other products from the same brands as the products tracked in the order, attributed to an ad.

Report types: dspProduct

clickToApplyBrandHaloClicks
Type: Integer

Description: The number of Click to apply clicks attributed to ad click-throughs. These include clicks on other products from the same brands as the ASINs tracked in the order.

Report types: dspProduct

clickToApplyBrandHaloViews
Type: Integer

Description: The number of Click to apply clicks attributed to impressions. These include clicks on other products from the same brands as the ASINs tracked in the order.

Report types: dspProduct

clickToApplyClicks
Type: Integer

Description: The number of click to apply conversions attributed to ad click-throughs.

Report types: dspProduct, dspTech, dspGeo, dspAudience

clickToApplyConversionRate
Type: Decimal

Description: The number of Click to apply conversions relative to the number of impressions. (CTAR = CTA / Impressions)

Report types: dspAudience

clickToApplyViews
Type: Integer

Description: The number of Click to apply conversions attributed to ad impressions.

Report types: dspProduct, dspTech, dspGeo, dspAudience

combinedECPP
Type: Decimal

Description: Effective (average) cost to acquire a purchase conversion on or off Amazon. (Total cost / Combined purchases)

Report types: dspCampaign, dspInventory

combinedERPM
Type: Decimal

Description: Effective (average) revenue for sales on and off Amazon generated per thousand impressions. (Combined Sales / (Impressions / 1000))

Report types: dspCampaign, dspInventory

combinedProductSales
Type: Integer

Description: Sales (in local currency) for purchases on and off Amazon, attributed to an ad view or click.

Report types: dspCampaign, dspInventory, dspGeo, dspTech

combinedPurchaseRate
Type: Decimal

Description: Rate of attributed purchase events on and off Amazon, relative to ad impressions. (Combined purchases / Impressions)

Report types: dspCampaign, dspInventory

combinedPurchases
Type: Integer

Description: Number of purchase events on and off Amazon, attributed to an ad view or click. (Off-Amazon purchases + Total purchases (Amazon))

Report types: dspCampaign, dspInventory, dspGeo

combinedPurchasesClicks
Type: Integer

Description: Number of purchase events on and off Amazon, attributed to an ad click. (Off-Amazon purchases clicks + Total purchases clicks (Amazon))

Report types: dspCampaign, dspInventory, dspGeo

combinedPurchasesViews
Type: Integer

Description: Number of purchase events on and off Amazon, attributed to an ad view. (Off-Amazon purchases views + Total purchases views (Amazon))

Report types: dspCampaign, dspInventory, dspGeo

combinedROAS
Type: Decimal

Description: Return on advertising spend for products sold on and off Amazon, measured as ad-attributed sales per local currency unit of ad spend. (Combined product sales / Total cost)

Report types: dspCampaign, dspInventory

combinedUnitsSold
Type: Integer

Description: Units of product sold on and off Amazon, attributed to an ad view or click. A single purchase event can include multiple sold units.

Report types: dspCampaign, dspInventory, dspGeo

completionRateVideoAd
Type: Decimal

Description: The number of video completions relative to the number of video starts. Completion rate (video) = complete views (video) / starts (video).

Report types: benchmarks

completionRateVideoAdP25
Type: Decimal

Description: The number of video completions relative to the number of video starts. It shows the performance of the bottom 25% peer brands.

Report types: benchmarks

completionRateVideoAdP50
Type: Decimal

Description: The number of video completions relative to the number of video starts. It shows the performance of the median 50% of peer brands, where half of the peer brands performed above and half of the brands performed below the median.

Report types: benchmarks

completionRateVideoAdP75
Type: Decimal

Description: The number of video completions relative to the number of video starts. It excludes the performance of the top 25% peer brands.

Report types: benchmarks

contact
Type: Integer

Description: The number of Contact conversions.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

contactCPA
Type: Decimal

Description: The average cost to acquire a Contact conversion. (Contact CPA = Total cost / Contact)

Report types: dspCampaign, dspInventory, dspAudience, dspGeo

contactCVR
Type: Decimal

Description: The number of Contact conversions relative to the number of ad impressions. (Contact CVR = Contact / Impressions)

Report types: dspCampaign, dspInventory, dspAudience, dspGeo

contactClicks
Type: Integer

Description: The number of Contact conversions attributed to an ad click.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

contactValueAverage
Type: Decimal

Description: Average value associated with a Contact conversion. (Contact value average = Contact value sum / Contact)

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

contactValueSum
Type: Decimal

Description: Sum of Contact conversion values

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

contactViews
Type: Integer

Description: The number of Contact conversions attributed to an ad view.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

contentCategory
Type String

Description: Content exclusion categories let you opt out of specific topics that don't align with your brand values.

Report types: dspBrandSuitability

contentGenre
Type: String

Description: Genre of the show where the ad impression was delivered. (e.g., Horror, Drama)

Report types: dspAudioAndVideo

contentRating
Type: String

Description: DSP content rating for parental guidance (e.g., "PG-13", "R")

Report types: dspAudioAndVideo

contentTitle
Type: String

Description: The name or title of the show/program where the audio or video ad was played.

Report types: dspAudioAndVideo

contentType
Type: String

Description: The content type of the show/program where the audio or video ad was played.

Report types: dspAudioAndVideo

conversionType
Type: String

Description: The conversion type describes whether the conversion happened on a promoted or a brand halo ASIN.

Report types: dspProduct

conversionsBrandHalo
Type: Integer

Description: For Sponsored Display vCPM campaigns, the total number of attributed conversion events occurring within 14 days of an ad click or view where the purchased SKU was different from the SKU advertised.

Report types: sdPurchasedProduct

conversionsBrandHaloClicks
Type: Integer

Description: For Sponsored Display vCPM campaigns, the total number of attributed conversion events occurring within 14 days of an ad click where the purchased SKU was different from the SKU advertised.

Report types: sdPurchasedProduct

cost
Type: Decimal

Description: Total cost of ad clicks.

Report types: spCampaigns, sbCampaigns, sbAdGroups, sbPlacement, spTargeting, sbTargeting, spSearchTerm, sbSearchTerm, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, stCampaigns, stTargeting, sbAds, spAdvertisedProduct, spGlobalAudiences, sbAudiences, spPromptAdExtension

costPerClick
Type: Decimal

Description: Total cost divided by total number of clicks.

Report types: spCampaigns, spTargeting, spSearchTerm, spAdvertisedProduct, spGlobalAudiences, sbAudiences, spPromptAdExtension

costPerCompletedViewVideoAd
Type: Decimal

Description: The average cost to acquire a video completion. Cost per completed view (video) = total cost / complete views (video).

Report types: benchmarks

costPerCompletedViewVideoAdP25
Type: Decimal

Description: The average cost to acquire a video completion. It shows the performance of the top 25% peer brands.

Report types: benchmarks

costPerCompletedViewVideoAdP50
Type: Decimal

Description: The average cost to acquire a video completion. It shows the performance of the median 50% of peer brands, where half of the peer brands performed above and half of the brands performed below the median.

Report types: benchmarks

costPerCompletedViewVideoAdP75
Type: Decimal

Description: The average cost to acquire a video completion. It excludes the performance of the bottom 25% peer brands.

Report types: benchmarks

costPerNewToBrandPurchase
Type: Decimal

Description: The average cost to acquire a purchase from a shopper who had not purchased a product from the brand in the last 12 months. Cost per purchase (new to brand) = total cost / purchases (new to brand).

Report types: benchmarks

costPerNewToBrandPurchaseP25
Type: Decimal

Description: The average cost to acquire a purchase from a shopper who had not purchased a product from the brand in the last 12 months. It shows the performance of the top 25% peer brands.

Report types: benchmarks

costPerNewToBrandPurchaseP50
Type: Decimal

Description: The average cost to acquire a purchase from a shopper who had not purchased a product from the brand in the last 12 months. It shows the performance of the median 50% of peer brands, where half of the peer brands performed above and half of the brands performed below the median.

Report types: benchmarks

costPerNewToBrandPurchaseP75
Type: Decimal

Description: The average cost to acquire a purchase from a shopper who had not purchased a product from the brand in the last 12 months. It excludes the performance of the bottom 25% peer brands.

Report types: benchmarks

costPerThousandImpressions
Type: Decimal

Description: The cost per thousand impressions.

Report types: stCampaigns, stTargeting, dspAudioAndVideo

costType
Type: String

Description: Determines how the campaign will bid and charge. One of vCPM (cost per thousand viewable impressions) or CPC (cost per click).

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sbSearchTerm, sdCampaigns, sbAds

country
Type: String

Description: Country.

Report types: dspGeo

cpc
Type: Decimal

Description: The average cost paid per click. Cost per click (CPC) = cost / clicks.

Report types: benchmarks

cpcP25
Type: Decimal

Description: The average cost paid per click. It shows the performance of the top 25% peer brands.

Report types: benchmarks

cpcP50
Type: Decimal

Description: The average cost paid per click. It shows the performance of the median 50% of peer brands, where half of the peer brands performed above and half of the brands performed below the median.

Report types: benchmarks

cpcP75
Type: Decimal

Description: The average cost paid per click. It excludes the performance of the bottom 25% peer brands.

Report types: benchmarks

cpm
Type: Decimal

Description: The total cost per thousand impressions. Cost per thousand impressions = (cost / impressions) * 1000.

Report types: benchmarks

cpmP25
Type: Decimal

Description: The total cost per thousand impressions. It shows the performance of the top 25% peer brands.

Report types: benchmarks

cpmP50
Type: Decimal

Description: The total cost per thousand impressions. It shows the performance of the median 50% of peer brands, where half of the peer brands performed above and half of the brands performed below the median.

Report types: benchmarks

cpmP75
Type: Decimal

Description: The total cost per thousand impressions. It excludes the performance of the bottom 25% peer brands.

Report types: benchmarks

creativeAdId
Type: String

Description: A unique identifier assigned to a creative. When this is different from creativeId, creativeAdId is the value that can be used in our /dsp/creatives endpoints.

Report types: dspCampaign

creativeExtensionId
Type: String

Description: A unique identifier for the creative extension associated with the ad.

Report types: spPromptAdExtension

creativeExtensionType
Type: String

Description: The type of creative extension (for example, PROMPTS).

Report types: spPromptAdExtension

creativeId
Type: String

Description: A unique identifier assigned to a creative. When this is different from creativeAdId, creativeId cannot be used in our /dsp/creatives endpoints.

Report types: dspCampaign, dspInventory, dspAudioAndVideo

creativeLanguage
Type: String

Description: The primary language in the creative.

Report types: dspCampaign

creativeName
Type: String

Description: Creative name.

Report types: dspCampaign, dspInventory, dspAudioAndVideo

creativeSize
Type: String

Description: The dimensions of the creative in pixels.

Report types: dspCampaign, dspInventory

creativeType
Type: String

Description: The type of creative (for example static image, third party, or video).

Report types: dspCampaign, dspInventory

creativeweight
Type: Integer

Description: This is typically represented as an integer percentage, ranging from 0 to 100. For example, 30 would represent 30% weight for a particular creative.

Report types: dspCampaign, dspInventory

ctr
Type: Decimal

Description: The percentage of impressions that were clicked. CTR = clicks / impressions.

Report types: benchmarks

ctrP25
Type: Decimal

Description: The percentage of impressions that were clicked. It shows the performance of the bottom 25% peer brands.

Report types: benchmarks

ctrP50
Type: Decimal

Description: The percentage of impressions that were clicked. It shows the performance of the median 50% of peer brands, where half of the peer brands performed above and half of the brands performed below the median.

Report types: benchmarks

ctrP75
Type: Decimal

Description: The percentage of impressions that were clicked. It excludes the performance of the top 25% peer brands.

Report types: benchmarks

cumulativeReach
Type: Integer

Description: Total number of unique users exposed to an ad from either a campaign, ad group, or product ad over the lifetime of the campaign or the past six months, whichever is shorter. This metric is updated daily.

Report types: sdCampaigns

date
Type: String

Description: Date when the ad activity ocurred in the format YYYY-MM-DD.

Report types: spCampaigns, sbCampaigns, sbAdGroups, sbPlacement, spTargeting, sbTargeting, spSearchTerm, sbSearchTerm, spPurchasedProduct, sbPurchasedProduct, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, sdPurchasedProduct, stCampaigns, stTargeting, spGrossandInvalids, sbGrossandInvalids, sdGrossandInvalids, sbAds, spAdvertisedProduct, dspCampaign, spGlobalAudiences, sbAudiences, dspReachFrequency,dspBidAdjustment, dspGeo, dspProduct, dspAudience, dspTech, dspInventory, benchmarks, spPromptAdExtension

deal
Type: String

Description: The name of a deal.

Report types: dspInventory

dealId
Type: String

Description: The unique identifier for the deal.

Report types: dspInventory

dealType
Type: String

Description: The type of a deal.

Report types: dspInventory

detailPageViewBrandHalo
Type: Integer

Description: Number of detail page views for products in your brand halo, attributed to an ad view or click. Use Total DPV to see all conversions for the brands' products.

Report types: dspProduct

detailPageViewBrandHaloClicks
Type: Integer

Description: Number of detail page views for products in your brand halo, attributed to an ad click. Use Total DPV clicks to see all conversions for the brands' products.

Report types: dspProduct

detailPageViewBrandHaloViews
Type: Integer

Description: Number of detail page views for products in your brand halo, attributed to an ad view. Use Total DPV views to see all conversions for the brands' products.

Report types: dspProduct

detailPageViewClicks
Type: Integer

Description: Number of detail page views for promoted products, attributed to an ad click. Use Total DPV clicks to see all conversions for the brands' products.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

detailPageViewRate
Type: Decimal

Description: Detail page view rate for promoted products relative to the number of ad impressions. (DPV / Impressions = DPVR) Use Total DPVR to see all conversions for the brands' products.

Report types: dspCampaign, dspInventory, dspAudience

detailPageViewRatePromotedClicks
Type: Decimal

Description: Rate of click-attributed detail page view conversions for promoted products relative to the number of ad impressions. (DPVR Clicks = DPV clicks / Impressions) Use Total DPV Click Rate to see all conversions for the brands' products.

Report types: dspAudience

detailPageViewViews
Type: Integer

Description: Number of detail page views for promoted products, attributed to an ad view. Use Total DPV views to see all conversions for the brands' products.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

detailPageViews
Type: Integer

Description: Number of detail page views occurring within 14 days of an ad click or view.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, stCampaigns, stTargeting, sbAds, dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

detailPageViewsClicks
Type: Integer

Description: Number of detail page views occurring within 14 days of an ad click.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, stCampaigns, stTargeting, sbAds
Type: String

Description: The Designated Market Areas¬¨¬®‚àö√ú (DMA) the customers were in when they viewed the ad. DMA regions are created and defined by Nielsen

Report types: dspGeo

dmaName
Type: String

Description: The Designated Market Areas¬¨¬®‚àö√ú (DMA) the customers were in when they viewed the ad. DMA regions are created and defined by Nielsen.

Report types: dspGeo

downloadedVideoPlayRate
Type: Decimal

Description: The number of downloaded video plays relative to the number of impressions. (Downloaded video play rate = Downloaded video plays / Impressions)

Report types: dspCampaign, dspInventory, dspAudience

downloadedVideoPlays
Type: Integer

Description: The number of times a video was downloaded then played for the featured product.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

downloadedVideoPlaysClicks
Type: Integer

Description: The number of downloaded video plays attributed to ad click-throughs.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

downloadedVideoPlaysViews
Type: Integer

Description: The number of downloaded video plays attributed to ad impressions.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

eCPAddToCart
Type: Decimal

Description: Effect cost per add to cart, calculated by cost divided by add-to-cart.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, sbAds, dspCampaign, dspInventory, dspAudience

eCPAddToList
Type: Decimal

Description: Effective (average) cost to acquire an Add to List conversion for a promoted product. (eCPATL = Total cost / ATL) Use Total eCPATL to see all conversions for the brands' products.

Report types: dspCampaign, dspInventory, dspAudience

eCPAddToWatchlist
Type: Decimal

Description: The average cost to acquire an Add to Watchlist click (eCPATW = Total cost / ATW)

Report types: dspCampaign, dspInventory, dspAudience

eCPAlexaSkillEnable
Type: Decimal

Description: The average cost to acquire an Alexa skill Enable conversion on a Kindle E Ink device. (eCP Alexa skill enable = Total cost / Alexa skill enable)

Report types: dspCampaign

eCPAppStoreFirstOpens
Type: Decimal

Description: The average cost to acquire a first-time app open. This is calculated as total cost divided by first app opens.

Report types: dspCampaign

eCPAppStoreOpens
Type: Integer

Description: The number of first-time and recurring app opens attributed to a click or view on an ad

Report types: dspCampaign

eCPAudioAdCompletion
Type: Decimal

Description: The average cost to acquire an audio complete conversion (eCPVC = Total cost / audio complete)

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

eCPBrandSearch
Type: Decimal

Description: Effective (average) cost to acquire a Branded Search.

Report types: sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

eCPC
Type: Decimal

Description: The average cost paid per click-through.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

eCPDetailPageView
Type: Decimal

Description: Effective (average) cost to acquire a detail page view for a promoted product. (eCPDPV = Total cost / DPV) Use Total eCPDPV to see all conversions for the brands' products.

Report types: dspCampaign, dspInventory, dspAudience

eCPDownloadedVideoPlays
Type: Decimal

Description: The average cost to acquire a downloaded video play (eCPDVP = Total cost / Downloaded video plays)

Report types: dspCampaign, dspInventory, dspAudience

eCPFreeTrialSubscriptionSignup
Type: Decimal

Description: The cost to acquire a free trial subscription for sponsored products. This is calculated as total cost divided by free trial subscription sign ups.

Report types: dspCampaign, dspInventory, dspAudience

eCPM
Type: Decimal

Description: The total cost per thousand impressions.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

eCPP
Type: Decimal

Description: Effective (average) cost to acquire a purchase conversion for a promoted product. (eCPP = Total cost / Purchases) Use Total eCPP to see all conversions for the brands' products.

Report types: dspCampaign, dspInventory, dspAudience

eCPPaidSubscriptionSignup
Type: Decimal

Description: The cost to acquire a paid subscription for sponsored products. This is calculated as total cost divided by paid subscription sign ups.

Report types: dspCampaign, dspInventory, dspAudience

eCPPlayTrailer
Type: Decimal

Description: The average cost to acquire a video trailer play (eCPPT = Total cost / Play trailers)

Report types: dspCampaign, dspInventory, dspAudience

eCPProductReviewPageVisit
Type: Decimal

Description: Effective (average) cost to acquire a product review page conversion for a promoted product. (eCPPRPV = Total cost / PRPV) Use Total eCPPRPV to see all conversions for the brands' products.

Report types: dspCampaign, dspInventory, dspAudience

eCPRental
Type: Decimal

Description: The average cost to acquire a rental (eCPR = Total cost / Rentals)

Report types: dspCampaign, dspInventory, dspAudience

eCPSkillInvocation
Type: Decimal

Description: Effective (average) cost to acquire a Skill invocation conversion for a promoted Alexa skill. (Effective cost per skill invocation = Total cost / Skill invocations)

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo

eCPSubscriptionSignup
Type: Decimal

Description: The cost to acquire a free trial or paid subscription for sponsored products. This is calculated as total cost divided by subscription sign ups.

Report types: dspCampaign, dspInventory, dspAudience

eCPVideoAdCompletion
Type: Decimal

Description: The average cost to acquire a Video complete conversion (eCPVC = Total cost / Video complete)

Report types: dspCampaign, dspInventory, dspAudience

eCPVideoDownload
Type: Decimal

Description: The average cost to acquire a video download (eCPVD = Total cost / Video downloads)

Report types: dspCampaign, dspInventory, dspAudience

eCPVideoStream
Type: Decimal

Description: The average cost to acquire a video stream. (eCPVS = Total cost / Video streams)

Report types: dspCampaign, dspInventory, dspAudience

eCPnewSubscribeAndSave
Type: Decimal

Description: Effective (average) cost to acquire a Subscribe & Save subscription for a promoted product. (eCPSnSS = Total cost / SnSS) Use Total eCPSnSS to see all conversions for the brands' products.

Report types: dspCampaign, dspInventory, dspAudience

eRPM
Type: Decimal

Description: Effective (average) revenue for promoted products generated per thousand impressions. (eRPM = Sales / (Impressions / 1000)) Use Total eRPM to see all conversions for the brands' products.

Report types: dspCampaign, dspInventory

effectiveCostPerDetailPageViewPromotedClicks
Type: Decimal

Description: Effective (average) cost to acquire a click-attributed detail page view conversion for a promoted product. (eCPDPV Clicks = Total cost / DPV clicks) Use Total eCPDPV Clicks to see all conversions for the brands' products.

Report types: dspAudience

effectiveCostPerPurchasePromotedClicks
Type: Decimal

Description: Effective (average) cost to acquire a click-attributed purchase for a promoted product. (eCPP Clicks = Total cost / Purchases clicks) Use Total eCPP Clicks to see all conversions for the brands' products.

Report types: dspAudience

effectiveCostPerSkillInvocation
Type: Decimal

Description: Effective (average) cost to acquire a Skill invocation conversion for a promoted Alexa skill. (Effective cost per skill invocation = Total cost / Skill invocations)

Report types: dspProduct, dspAudience

einkDetailPageView
Type: Integer

Description: The number of views of Ad Details pages on Kindle E Ink devices.

Report types: dspProduct

einkDetailPageViewBrandHalo
Type: Integer

Description: The number of Detail page views (Kindle) on other products from the same brands as the products tracked in the order, attributed to an ad.

Report types: dspProduct

einkDetailPageViewBrandHaloClicks
Type: Integer

Description: The number of Detail page views (Kindle) attributed to ad click-throughs. These include clicks on other products from the same brands as the ASINs tracked in the order.

Report types: dspProduct

einkDetailPageViewBrandHaloViews
Type: Integer

Description: The number of Detail page views (Kindle) attributed to impressions. These include clicks on other products from the same brands as the ASINs tracked in the order.

Report types: dspProduct

einkDetailPageViewClicks
Type: Integer

Description: The number of views of Ad Details pages on Kindle E Ink devices attributed to clicks on ads on Kindle E Ink devices.

Report types: dspProduct

einkDetailPageViewViews
Type: Integer

Description: The number of views of Ad Details pages on Kindle E Ink devices attributed to views on ads on Kindle E Ink devices

Report types: dspProduct

endDate
Type: String

Description: End date of summary period for a report in the format YYYY-MM-DD.

Report types: spCampaigns, sbCampaigns, sbAdGroups, sbPlacement, spTargeting, sbTargeting, spSearchTerm, sbSearchTerm, spPurchasedProduct, sbPurchasedProduct, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, sdPurchasedProduct, stCampaigns, stTargeting, spGrossandInvalids, sbGrossandInvalids, sdGrossandInvalids, sbAds, spAdvertisedProduct, spGlobalAudiences, sbAudiences, dspBidAdjustment, conversionPath, benchmarks, spPromptAdExtension

entityId
Type: String

Description: Entity (seat) ID.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspProduct, dspAudience

environmentName
Type: String

Description: Break the data down by which environment the bid request came from: web or app. This dimension is connected to web and app inventory, not line item types.

Report types: dspTech

exclusiveReachRate
Type: decimal

Description: This metric measures the percentage of users who were reached ONLY by this specific campaign/line item and were not reached by any other campaigns in your media plan. The exclusiveReachRate is particularly useful when you want to understand how many users are being reached solely by a specific campaign, which can help in assessing campaign overlap and media efficiency.

Report types: dspCampaign

featuredAsin
Type: String

Description: The Amazon Standard Identification Number (ASIN) that was set as featured in the campaign.

Report types: dspProduct

flightBudget
Type: Decimal

Description: The total budget of the campaign flight.

Report types: dspCampaign

flightEndDate
Type: String

Description: The end date of the campaign flight.

Report types: dspCampaign

flightId
Type: String

Description: The unique ID associated with a specific campaign flight to track and manage campaign delivery.

Report types: dspCampaign

flightName
Type: String

Description: The name of the campaign flight.

Report types: dspCampaign

flightStartDate
Type: String

Description: The start date of the campaign flight.

Report types: dspCampaign

freeTrialSubscriptionSignupClicks
Type: Integer

Description: The number of free trial subscriptions for sponsored products associated with a click on your ad.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

freeTrialSubscriptionSignupRate
Type: Decimal

Description: The ratio of how often customers signed up for a free trial for sponsored products when you ad was displayed. This is calculated as free trials divided by impressions.

Report types: dspCampaign, dspInventory, dspAudience

freeTrialSubscriptionSignupViews
Type: Integer

Description: The number of free trial subscriptions for sponsored products associated with ad impressions.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

freeTrialSubscriptionSignups
Type: Integer

Description: The number of free trial subscriptions for sponsored products associated with a click or view on your ad.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

frequencyAverage
Type: Decimal

Description: The number of times an ad is served to an individual/ device/ account in a period.

Report types: stCampaigns, dspCampaign, dspReachFrequency

frequencyGroupId
Type: Long

Description: The identifier of the frequency group.

Report types: dspReachFrequency

frequencyGroupName
Type: String

Description: The name of the frequency group as entered by the advertiser.

Report types: dspReachFrequency

grossClickThroughs
Type: Integer

Description: The total number of times the ad was clicked. This includes valid, potentially fraudulent, non-human, and other illegitimate clicks.

Report types: spGrossandInvalids, sbGrossandInvalids, sdGrossandInvalids, dspCampaign, dspInventory, dspGeo, dspTech, dspAudience

grossImpressions
Type: Integer

Description: The total number of times the ad was displayed. This includes valid and invalid impressions such as potentially fraudulent, non-human, and other illegitimate impressions.

Report types: spGrossandInvalids, sbGrossandInvalids, sdGrossandInvalids, dspCampaign, dspInventory, dspGeo, dspAudioAndVideo, dspTech, dspAudience

householdFrequencyAverage
Type: Decimal

Description: The number of times an ad is served to a household in a period.

Report types: stCampaigns, dspCampaign

householdReach
Type: Integer

Description: The number of unique households an ad impression is served to in a period.

Report types: stCampaigns, dspCampaign

impressionFrequencyAverage
Type: Decimal

Description: The average number of exposures per unique user for an ad

Report types: dspCampaign

impressions
Type: Integer

Description: Total number of ad impressions.

Report types: spCampaigns, sbCampaigns, sbAdGroups, sbPlacement, spTargeting, sbTargeting, spSearchTerm, sbSearchTerm, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, stCampaigns, stTargeting, spGrossandInvalids, sbGrossandInvalids, sdGrossandInvalids, sbAds, spAdvertisedProduct, dspCampaign, dspInventory, dspTech, dspGeo, dspAudience, dspAudioAndVideo, spGlobalAudiences, sbAudiences, dspProduct, spPromptAdExtension

impressionsFrequencyAverage
Type: Decimal

Description: Average number of times unique users were exposed to an ad over the lifetime of the campaign.

Report types: sdCampaigns, sdAdGroups, sdAdvertisedProduct

impressionsViews
Type: Integer

Description: Number of impressions that met the Media Ratings Council (MRC) viewability standard. See viewability details at https://advertising.amazon.com/library/guides/viewability.

Report types: sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct

incrementalReachRate
Type: decimal

Description: This metric represents the percentage of unique users reached by your campaign who were not reached by other campaigns in your media plan.

Report types: dspCampaign

interactiveImpressions
Type: Integer

Description: The number of impressions from an interactive creative. This includes, interactive video, interactive audio and interactive display creatives, and more.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

intervalEnd
Type: String

Description: End date of report data.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience, dspAudioAndVideo, dspReachFrequency

intervalStart
Type: String

Description: Start date of report data.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience, dspAudioAndVideo, dspReachFrequency

invalidClickThroughRate
Type: Decimal

Description: The percentage of gross click-throughs that were removed by the traffic quality filter. (Invalid click-throughs rate = invalid click-throughs / gross click-throughs)

Report types: spGrossandInvalids, sbGrossandInvalids, sdGrossandInvalids, dspCampaign, dspInventory, dspGeo, dspAudience

invalidClickThroughs
Type: Integer

Description: Clicks that were removed by the traffic quality filter. This includes potentially fraudulent, non-human, and other illegitimate traffic.

Report types: spGrossandInvalids, sbGrossandInvalids, sdGrossandInvalids, dspCampaign, dspInventory, dspGeo, dspTech, dspAudience

invalidImpressionRate
Type: Decimal

Description: The percentage of gross impressions that were removed by the traffic quality filter. (Invalid impression rate = invalid impressions / gross impressions)

Report types: spGrossandInvalids, sbGrossandInvalids, sdGrossandInvalids, dspCampaign, dspInventory, dspGeo, dspTech, dspAudience

invalidImpressions
Type: Integer

Description: The number of impressions removed by a traffic quality filter. This includes potentially fraudulent, non-human, and other illegitimate traffic.

Report types: spGrossandInvalids, sbGrossandInvalids, sdGrossandInvalids, dspCampaign, dspInventory, dspGeo, dspAudioAndVideo, dspTech, dspAudience

inventoryTier
Type: String

Description: Inventory tiers group ad-eligible inventory to help you balance reach with brand suitability preferences.

Report types: dspBrandSuitability

keyword
Type: String

Description: Text of the keyword or a representation of the targeting expression (for Sponsored Products). For Sponsored Products targeting reports, the same value is returned in the targeting metric.

Report types: spTargeting, spSearchTerm, spPurchasedProduct, stTargeting

keywordBid
Type: Decimal

Description: Bid associated with a keyword or targeting expression.

Report types: spTargeting, sbTargeting, spSearchTerm, sbSearchTerm, stTargeting

keywordId
Type: Integer

Description: ID associated with a keyword or targeting expression.

Report types: spTargeting, sbTargeting, spSearchTerm, sbSearchTerm, spPurchasedProduct, stTargeting

keywordText
Type: String

Description: Text of the keyword.

Report types: sbTargeting, sbSearchTerm

keywordType
Type: String

Description: Type of matching for the keyword used in bid. For keywords, one of: BROAD, PHRASE, or EXACT. For Sponsored Products reports, keywordType can also contain the type of targeting expressions, one of: TARGETINGEXPRESSION or TARGETINGEXPRESSION_PREDEFINED.

Report types: spTargeting, sbTargeting, spSearchTerm, spPurchasedProduct, stTargeting

kindleDetailPageView
Type: String

Description: The number of views of Ad Details pages on Kindle E Ink devices.

Report types: dspTech, dspGeo, dspAudience

kindleDetailPageViewClicks
Type: Integer

Description: The number of views of Ad Details pages on Kindle E Ink devices attributed to clicks on ads on Kindle E Ink devices.

Report types: dspTech, dspGeo, dspAudience

kindleDetailPageViewRate
Type: Decimal

Description: The number of views of the Ad Details page relative to the number of ad impressions on Kindle E Ink devices. (DPVKR = DPVK / Impressions)

Report types: dspAudience

kindleDetailPageViewViews
Type: Integer

Description: The number of views of Ad Details pages on Kindle E Ink devices attributed to views on ads on Kindle E Ink devices

Report types: dspTech, dspGeo, dspAudience

kindleEditionNormalizedPagesRead
Type: Integer

Description: Number of attributed Kindle edition normalized pages read within 14 days of ad click or ad view.

Report types: sdAdGroup, sdAdvertisedProduct, sdCampaigns, sdPurchasedProduct, sdTargeting

kindleEditionNormalizedPagesReadFromClicks
Type: Integer

Description: Number of attributed Kindle edition normalized pages read within 14 days of ad click.

Report types: sdAdGroup, sdAdvertisedProduct, sdCampaigns, sdPurchasedProduct, sdTargeting

kindleEditionNormalizedPagesReadFromViews
Type: Integer

Description: Number of attributed Kindle edition normalized pages read within 14 days of ad view.

Report types: sdAdGroup, sdAdvertisedProduct, sdCampaigns, sdPurchasedProduct, sdTargeting

kindleEditionNormalizedPagesRead14d
Type: Integer

Description: Number of attributed Kindle edition normalized pages read within 14 days of ad click.

Report types: spCampaigns, spTargeting, spSearchTerm, spPurchasedProduct, spAdvertisedProduct, sbCampaigns, sbAdGroup, sbAds, sbCampaignPlacement, sbPurchasedProduct, sbSearchTerm

kindleEditionNormalizedPagesRoyalties
Type: Decimal

Description: The estimated royalties of attributed estimated Kindle edition normalized pages within 14 days of ad click or ad view.

Report types: sdAdGroup, sdAdvertisedProduct, sdCampaigns, sdPurchasedProduct, sdTargeting

kindleEditionNormalizedPagesRoyaltiesFromClicks
Type: Decimal

Description: The estimated royalties of attributed estimated Kindle edition normalized pages within 14 days of ad click.

Report types: sdAdGroup, sdAdvertisedProduct, sdCampaigns, sdPurchasedProduct, sdTargeting

kindleEditionNormalizedPagesRoyaltiesFromViews
Type: Decimal

Description: The estimated royalties of attributed estimated Kindle edition normalized pages within 14 days of ad view.

Report types: sdAdGroup, sdAdvertisedProduct, sdCampaigns, sdPurchasedProduct, sdTargeting

kindleEditionNormalizedPagesRoyalties14d
Type: Decimal

Description: The estimated royalties of attributed estimated Kindle edition normalized pages within 14 days of ad click.

Report types: spCampaigns, spTargeting, spSearchTerm, spPurchasedProduct, spAdvertisedProduct, sbCampaigns, sbAdGroup, sbAds, sbCampaignPlacement, sbPurchasedProduct, sbSearchTerm

lead
Type: Integer

Description: The number of Lead conversions.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

leadCPA
Type: Decimal

Description: The average cost to acquire a Lead conversion. (Lead CPA = Total cost / Lead)

Report types: dspCampaign, dspInventory, dspAudience

leadCVR
Type: Decimal

Description: The number of Lead conversions relative to the number of ad impressions. (Lead CVR = Lead / Impressions)

Report types: dspCampaign, dspInventory, dspAudience

leadClicks
Type: Integer

Description: The number of Lead conversions attributed to an ad click.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

leadValueAverage
Type: Decimal

Description: Average value associated with a Lead conversion. (Lead value average = Lead value sum / Lead)

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

leadValueSum
Type: Decimal

Description: Sum of Lead conversion values

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

leadViews
Type: Integer

Description: The number of Lead conversions attributed to an ad view.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

lineItemApprovalStatus
Type: String

Description: Approval status for the line item

Report types: dspCampaign

lineItemBudget
Type: Decimal

Description: The total amount of money that be consumed by a line item.

Report types: dspCampaign, dspInventory, dspProduct, dspGeo

lineItemBudgetCap
Type: Decimal

Description: The total budget set for the line item.

Report types: dspCampaign

lineItemComment
Type: String

Description: Comments entered about the line item, such as optimization changes, variations in targeting, etc.

Report types: dspCampaign

lineItemComments
Type: String

Description: Comments entered about the line item, such as optimization changes, variations in targeting, etc.

Report types: dspInventory, dspProduct, dspTech, dspGeo, dspAudience

lineItemDeliveryRate
Type: Decimal

Description: Delivery Rate of the order. Delivery Rate = (cost/budget)/(running days/total days) or (delivery impressions/budget impressions)/(running days/total days)

Report types: dspCampaign

lineItemEndDate
Type: String

Description: The last date for the line item's flight.

Report types: dspCampaign, dspInventory, dspProduct, dspGeo, dspAudience

lineItemExternalId
Type: String

Description: Line item custom ID optionally entered by user.

Report types: dspCampaign, dspInventory, dspProduct

lineItemId
Type: String

Description: A unique identifier assigned to a line item.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience, dspAudioAndVideo, dspBidAdjustment

lineItemLanguageTargeting
Type: String

Description: The language targeting setting for the line item.

Report types: dspCampaign

lineItemName
Type: String

Description: Line item name.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience, dspAudioAndVideo, dspBidAdjustment

lineItemStartDate
Type: String

Description: The first date for the line item's flight.

Report types: dspCampaign, dspInventory, dspProduct, dspGeo, dspAudience

lineItemStatus
Type: String

Description: Status of the ad/line item

Report types: dspCampaign

lineItemType
Type: String

Description: Type of the ad/line item

Report types: dspCampaign, dspAudience

linkOuts
Type: Integer

Description: The number of times link-outs to landing page were clicked.

Report types: sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct

longTermSales
Type Decimal

Description The 12 month potential value of new-to-brand customer-brand engagements (DPV, Branded Search, ATC, Purchase) based on the average return on engagement of shoppers who completed these same actions 12 months ago with your brand, plus the campaign's 14d total sales.

Report types: sdCampaigns, sbCampaigns, stCampaigns, dspCampaign

longTermROAS
Type Decimal

Description The 12 month potential return on ad spend of new-to-brand customer-brand engagements (DPV, Branded Search, ATC, Purchase) based on the average return on engagement of shoppers who completed these same actions 12 months ago with your brand, plus the campaign's 14d total sales. Long-term ROAS = (Long-term Sales / Total cost)

Report types: sdCampaigns, sbCampaigns, stCampaigns, dspCampaign

marketplace
Type: String

Description: The Amazon-owned site the product is sold on.

Report types: dspCampaign, dspInventory, dspProduct, spGlobalAudiences, sbAudiences, spPromptAdExtension

masterClicks
Type: Integer

Description: A click on a master advertisement that directs the user to a destination outside of the creative.

Report types: dspAudience

masterImpressions
Type: Integer

Description: The number of times the master advertisement was displayed.

Report types: dspAudience

matchRate
Type: Decimal

Description: The percentage of eligible bid requests that matched with the bid adjustment terms. The values range from 0 to 100 where 100 represents 100%.

Report types: dspBidAdjustment

matchType
Type: String

Description: Type of matching for the keyword used in bid. For keywords, one of: BROAD, PHRASE, or EXACT. For Sponsored Products reports, keywordType can also contain the type of targeting expressions, one of: TARGETINGEXPRESSION or TARGETINGEXPRESSION_PREDEFINED.

 Note
The Amazon Ads Console uses "-" in place of TARGETING_EXPRESSION or TARGETING_EXPRESSION_PREDEFINED in generated reports.
Report types: spTargeting, sbTargeting, spSearchTerm, sbSearchTerm, spPurchasedProduct, stTargeting

matchedTargetAsin
Type: String

Description: The ASIN associated with the product page where a Sponsored Display ad appeared.

Report types: sdCampaigns, sdAdGroups, sdTargeting

measurableImpressions
Type: Integer

Description: Number of impressions that were measured for viewability. The viewability metrics are available from October 1, 2019. Selecting a date range prior to October 1, 2019 will result in incomplete or inaccurate metrics.

Report types: dspCampaign, dspInventory

measurableRate
Type: Decimal

Description: Measurable impressions / total impressions. The viewability metrics are available from October 1, 2019. Selecting a date range prior to October 1, 2019 will result in incomplete or inaccurate metrics.

Report types: dspCampaign, dspInventory

mobileAppFirstStartAverage
Type: Decimal

Description: Average value associated with a Mobile app first start conversion. (Mobile app first start value average = Mobile app first start value sum / Mobile app first start)

Report types: dspTech, dspGeo

mobileAppFirstStartCPA
Type: Decimal

Description: The average cost to acquire a Mobile app first start conversion. (Mobile app first start CPA = Total cost / Mobile app first starts)

Report types: dspCampaign, dspInventory, dspAudience

mobileAppFirstStartCVR
Type: Decimal

Description: The number of Mobile app first start conversions relative to the number of ad impressions. (Mobile app first start CVR = Mobile app first start / Impressions)

Report types: dspCampaign, dspInventory, dspAudience

mobileAppFirstStartClicks
Type: Integer

Description: The number of Mobile app first start conversions attributed to ad click-throughs.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

mobileAppFirstStartSum
Type: Decimal

Description: Sum of Mobile app first start conversion values

Report types: dspTech, dspGeo

mobileAppFirstStartViews
Type: Integer

Description: The number of Mobile app first start conversions attributed to ad impressions.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

mobileAppFirstStarts
Type: Integer

Description: The number of times an app for the featured product was first started.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

newSubscribeAndSave
Type: Integer

Description: Number of new Subscribe & Save subscriptions for all products, attributed to an ad view or click. This does not include replenishment subscription orders. Use Total SnSS to see all conversions for the brands' products.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

newSubscribeAndSaveBrandHalo
Type: Integer

Description: Number of new Subscribe & Save subscriptions for brand halo products, attributed to an ad view or click. This does not include replenishment subscription orders. Use Total SnSS to see all conversions for the brands' products.

Report types: dspProduct

newSubscribeAndSaveBrandHaloClicks
Type: Integer

Description: Number of new Subscribe & Save subscriptions for brand halo products, attributed to an ad click. This does not include replenishment subscription orders. Use Total SnSS clicks to see all conversions for the brands' products.

Report types: dspProduct

newSubscribeAndSaveBrandHaloViews
Type: Integer

Description: Number of new Subscribe & Save subscriptions for brand halo products, attributed to an ad view. This does not include replenishment subscription orders. Use Total SnSS views to see all conversions for the brands' products.

Report types: dspProduct

newSubscribeAndSaveClicks
Type: Integer

Description: Number of new Subscribe & Save subscriptions for all products, attributed to ad clicks. This does not include replenishment subscription orders. Use Total SnSS to see all conversions for the brands' products.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

newSubscribeAndSaveRate
Type: Decimal

Description: The number of new Subscribe & Save subscriptions relative to the number of ad impressions

Report types: dspCampaign, dspInventory, dspAudience

newSubscribeAndSaveViews
Type: Integer

Description: Number of new Subscribe & Save subscriptions for all products, attributed to ad views. This does not include replenishment subscription orders. Use Total SnSS to see all conversions for the brands' products.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

newToBrandDetailPageViewClicks
Type: Integer

Description: Number of new-to-brand detail page views for all the brands' products, attributed to an ad click.

Report types: sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, stCampaigns, stTargeting, dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

newToBrandDetailPageViewRate
Type: Decimal

Description: Calculated by dividing newToBrandDetailPageViews / impressions.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, sbAds, dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

newToBrandDetailPageViewViews
Type: Integer

Description: Number of new-to-brand detail page views for all the brands' products, attributed to an ad view

Report types: sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, stCampaigns, stTargeting, dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

newToBrandDetailPageViews
Type: Integer

Description: The number of new detail page views from shoppers who have not previously viewed a detail page with an ASIN of the same brand in past 365 days and who either clicked or viewed an ad.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, stCampaigns, stTargeting, sbAds, dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

newToBrandDetailPageViewsClicks
Type: Integer

Description: The number of new detail page views from shoppers who have not previously viewed a detail page with an ASIN of the same brand in past 365 days and who clicked an ad.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sbAds

newToBrandECPDetailPageView
Type: Decimal

Description: Effective cost per new-to-brand detail page view, calculated by cost divided by new-to-brand detail page view.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, sbAds, dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

brandStorePageView
Type: Integer

Description: The number of Brand Store pages that were viewed and attributed to your ads.

Report types: sbCampaigns

newToBrandERPM
Type: Decimal

Description: Effective (average) revenue generated per thousand impressions from promoted products purchased by new-to-brand shoppers. (NTB eRPM = NTB Sales / (Impressions / 1000)) Use Total new-to-brand eRPM to see all conversions for the brands' products.

Report types: dspCampaign, dspInventory

newToBrandProductSales
Type: Integer

Description: Sales (in local currency) of promoted products to new-to-brand shoppers, attributed to an ad view or click. Use Total new-to-brand product sales to see all conversions for the brands' products.

Report types: dspCampaign, dspInventory, dspGeo, dspProduct, dspTech

newToBrandPurchasePercentageBrandHalo
Type: Decimal

Description: Percent of ad-attributed purchases for brand halo products that were new to brand. Use Total percent of purchases new-to-brand to see all conversions for the brands' products.

Report types: dspProduct

newToBrandPurchaseRate
Type: Decimal

Description: Rate of new-to-brand purchase conversions for promoted products relative to the number of ad impressions. (New-to-brand purchase rate = New-to-brand purchases / Impressions) Use Total new-to-brand purchase rate to see all conversions for the brands' products.

Report types: dspCampaign, dspInventory, dspAudience, benchmarks

newToBrandPurchaseRateP25
Type: Decimal

Description: The rate of new-to-brand purchases relative to ad impressions. It shows the performance of the bottom 25% peer brands.

Report types: benchmarks

newToBrandPurchaseRateP50
Type: Decimal

Description: The rate of new-to-brand purchases relative to ad impressions. It shows the performance of the median 50% of peer brands, where half of the peer brands performed above and half of the brands performed below the median.

Report types: benchmarks

newToBrandPurchaseRateP75
Type: Decimal

Description: The rate of new-to-brand purchases relative to ad impressions. It excludes the performance of the top 25% peer brands.

Report types: benchmarks

newToBrandPurchases
Type: Integer

Description: The number of first-time orders for brand products over a one-year lookback window resulting from an ad click or view. Not available for book vendors.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, stCampaigns, stTargeting, sbAds, dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience, conversionPath

newToBrandPurchases14d
Type: Integer

Description: The number of first-time orders for brand products over a one-year lookback window. Not available for book vendors.

Report types: sbPurchasedProduct

newToBrandPurchasesBrandHalo
Type: Integer

Description: Number of new-to-brand purchases for brand halo products, attributed to an ad view or click. Shoppers are "new to brand" if they have not purchased from the brand in the last 365 days. Use Total new-to-brand purchases to see all conversions for the brands' products.

Report types: dspProduct

newToBrandPurchasesBrandHaloClicks
Type: Integer

Description: Number of new-to-brand purchases for brand halo products, attributed to an ad click. Shoppers are "new to brand" if they have not purchased from the brand in the last 365 days. Use Total new-to-brand purchases clicks to see all conversions for the brands' products.

Report types: dspProduct

newToBrandPurchasesBrandHaloViews
Type: Integer

Description: Number of new-to-brand purchases for brand halo products, attributed to an ad view. Shoppers are "new to brand" if they have not purchased from the brand in the last 365 days. Use Total new-to-brand purchases views to see all conversions for the brands' products.

Report types: dspProduct

newToBrandPurchasesClicks
Type: Integer

Description: The number of first-time orders for brand products over a one-year lookback window resulting from an ad click. Not available for book vendors.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, stCampaigns, stTargeting, sbAds, dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

newToBrandPurchasesPercentage
Type: Decimal

Description: The percentage of total orders that are new-to-brand orders within 14 days of an ad click. Not available for book vendors.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sbAds, dspCampaign, dspProduct, dspAudience

newToBrandPurchasesPercentage14d
Type: Decimal

Description: The percentage of total orders that are new-to-brand orders within 14 days of an ad click. Not available for book vendors.

Report types: sbPurchasedProduct

newToBrandPurchasesRate
Type: Decimal

Description: The percentage of total orders that are new-to-brand orders. Not available for book vendors.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sbAds

newToBrandPurchasesViews
Type: Integer

Description: The number of new to branch purchases attributed to an ad view.

Report types: stCampaigns, stTargeting, dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

newToBrandROAS
Type: Decimal

Description: Return on ad spend for new to brand sales

Report types: dspCampaign, dspInventory

newToBrandSales
Type: Decimal

Description: Total value of new-to-brand sales occurring within 14 days of an ad click or view. Not available for book vendors.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, stCampaigns, stTargeting, sbAds, conversionPath

newToBrandSales14d
Type: Decimal

Description: Total value of new-to-brand sales occurring within 14 days of an ad click. Not available for book vendors.

Report types: sbPurchasedProduct

newToBrandSalesClicks
Type: Decimal

Description: Total value of new-to-brand sales occurring within 14 days of an ad click. Not available for book vendors.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, stCampaigns, stTargeting, sbAds

newToBrandSalesPercentage
Type: Decimal

Description: Percentage of total sales made up of new-to-brand purchases within 14 days of an ad click. Not available for book vendors. Same as newToBrandSalesPercentage14d.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sbAds

newToBrandSalesPercentage14d
Type: Decimal

Description: Percentage of total sales made up of new-to-brand purchases within 14 days of an ad click. Not available for book vendors. Same as newToBrandSalesPercentage.

Report types: sbPurchasedProduct

newToBrandSalesViews
Type: Decimal

Description: Total value of sales by new to brand customers occurring within 14 days of an ad view.

Report types: stCampaigns, stTargeting

newToBrandUnitsSold
Type: Integer

Description: Total number of attributed units ordered as part of new-to-brand sales occurring within 14 days of an ad click or view. Not available for book vendors.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, sbAds, dspCampaign, dspInventory, dspProduct, dspGeo, dspTech

newToBrandUnitsSold14d
Type: Integer

Description: Total number of attributed units ordered as part of new-to-brand sales occurring within 14 days of an ad click or view. Not available for book vendors.

Report types: sbPurchasedProduct

newToBrandUnitsSoldBrandHalo
Type: Integer

Description: Units of brand halo products purchased by new-to-brand shoppers, attributed to an ad view or click. A new-to-brand purchase event can include multiple sold units. Use Total new-to-brand units sold to see all conversions for the brands' products.

Report types: dspProduct

newToBrandUnitsSoldClicks
Type: Integer

Description: Total number of attributed units ordered as part of new-to-brand sales occurring within 14 days of an ad click. Not available for book vendors.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, sbAds

newToBrandUnitsSoldPercentage
Type: Decimal

Description: Percentage of total attributed units ordered within 14 days of an ad click that are part of a new-to-brand purchase. Not available for book vendors. Same as newToBrandUnitsSoldPercentage14d.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sbAds

newToBrandUnitsSoldPercentage14d
Type: Decimal

Description: Percentage of total attributed units ordered within 14 days of an ad click that are part of a new-to-brand purchase. Not available for book vendors. Same as newToBrandUnitsSoldPercentage.

Report types: sbPurchasedProduct

notificationClicks
Type: Integer

Description: The number of times the link inside an email or push notification was opened.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

notificationOpens
Type: Integer

Description: The number of times an email or push notification was opened.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

offAmazonCPA
Type: Decimal

Description: The average cost to acquire for Off Amazon conversions

Report types: dspCampaign, dspInventory, dspAudience

offAmazonCVR
Type: Decimal

Description: Number of off-Amazon conversions relative to the number of ad impressions. (Off-Amazon conversions / Impressions)

Report types: dspCampaign, dspInventory, dspAudience

offAmazonClicks
Type: Integer

Description: Number of conversions that occured off Amazon attributed to an ad click. This includes all conversion types.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

offAmazonConversions
Type: Integer

Description: Number of conversions that occured off Amazon attributed to an ad view or click. This includes all conversion types.

Report types: dspCampaign, dspInventory, dspGeo, dspAudience, dspTech

offAmazonECPP
Type: Decimal

Description: Effective (average) cost to acquire an off-Amazon purchase event. (Total cost / Off-Amazon purchases)

Report types: dspCampaign, dspInventory, dspAudience

offAmazonERPM
Type: Decimal

Description: Effective (average) revenue for sales included in off-Amazon purchases generated per thousand impressions. (Off-Amazon sales / (Impressions / 1000))

Report types: dspCampaign, dspInventory

offAmazonProductSales
Type: Decimal

Description: Sales (in local currency) of promoted products to off Amazon shoppers, attributed to an ad view or click.

Report types: dspCampaign, dspInventory, dspTech, dspGeo

offAmazonPurchaseRate
Type: Decimal

Description: Rate of attributed off-Amazon purchase events relative to ad impressions. (Off-Amazon purchases / Impressions)

Report types: dspCampaign, dspInventory, dspAudience

offAmazonPurchases
Type: Decimal

Description: Off Amazon Purchases

Report types: dspCampaign, dspInventory, dspGeo, dspTech

offAmazonPurchasesClicks
Type: Integer

Description: Number of off-Amazon purchase events attributed to an ad click.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

offAmazonPurchasesViews
Type: Integer

Description: Number of off-Amazon purchase events attributed to an ad view.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

offAmazonROAS
Type: Decimal

Description: Return on ad spend for off Amazon sales

Report types: dspCampaign, dspInventory

offAmazonUnitsSold
Type: Integer

Description: Units of product purchased off Amazon, attributed to an ad view or click. A single purchase event can include multiple sold units.

Report types: dspCampaign, dspInventory, dspGeo

offAmazonViews
Type: Integer

Description: Number of conversions that occured off Amazon attributed to an ad view. This includes all conversion types.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

omnichannelMetricsFee
Type: Decimal

Description: This fee is calculated based on a percentage of the supply cost

Report types: dspCampaign

omsLineItemId
Type: String

Description: A unique identifier for a line item imported from the Amazon Order Management System (OMS).

Report types: dspProduct, dspTech, dspGeo, dspAudience

omsProposalId
Type: String

Description: A unique identifier for an order imported from the Amazon Order Management System (OMS).

Report types: dspProduct, dspAudience

onTargetCostPerImpression
Type: Decimal

Description: The total cost per thousand on-target impressions

Report types: dspCampaign

onTargetCPM
Type: Decimal

Description: The actual cost per thousand impressions (CPM) for impressions that reached your intended target audience.

Report types: dspCampaign

onTargetImpressionCost
Type: Decimal

Description: The total amount of money spent on the campaign when delivering on-target impressions

Report types: dspCampaign

onTargetImpressions
Type: Integer

Description: The number of times an advertisement was displayed within the advertiser’s target demographic segment, as measured by Nielsen Digital Ad Ratings

Report types: dspCampaign

operatingSystemName
Type: String

Description: The operating systems the customers used to view the ad

Report types: dspTech

orderBudget
Type: Decimal

Description: The total amount of money that be consumed by an order.

Report types: dspCampaign, dspInventory, dspProduct, dspGeo

orderCurrency
Type: String

Description: Order currency.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

orderEndDate
Type: String

Description: The last day a line item within an order is eligible to run.

Report types: dspCampaign, dspInventory, dspProduct, dspGeo, dspAudience

orderExternalId
Type: String

Description: Order External ID or PO number

Report types: dspCampaign, dspInventory, dspProduct

orderId
Type: String

Description: A unique identifier assigned to an order.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience, dspAudioAndVideo, dspBidAdjustment

orderName
Type: String

Description: Order name.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience, dspAudioAndVideo, dspBidAdjustment

orderStartDate
Type: String

Description: The first day a line item within an order is eligible to run.

Report types: dspCampaign, dspInventory, dspProduct, dspGeo, dspAudience

orders14d
Type: Integer

Description: Number of orders within the last 14 days. Includes orders attributed to both clicks and views for vCPM campaigns, but only sales attributed to clicks for CPC campaigns.

Report types: sbPurchasedProduct

ordersClicks14d
Type: Integer

Description: Number of orders within the last 14 days attributed to ad clicks.

Report types: sbPurchasedProduct

other
Type: Integer

Description: The number of Other conversions.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

otherCPA
Type: Decimal

Description: The average cost to acquire an Other conversion. (Other CPA = Total cost / Other)

Report types: dspCampaign, dspInventory, dspAudience

otherCVR
Type: Decimal

Description: The number of Other conversions relative to the number of ad impressions. (Other CVR = Other / Impressions)

Report types: dspCampaign, dspInventory, dspAudience

otherClicks
Type: Integer

Description: The number of Other conversions attributed to an ad click.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

otherValueAverage
Type: Decimal

Description: Average value associated with an Other conversion. (Other value average = Other value sum / Other)

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

otherValueSum
Type: Decimal

Description: Sum of Other conversion values

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

otherViews
Type: Integer

Description: The number of Other conversions attributed to an ad view.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

pageViewCPA
Type: Decimal

Description: The average cost to acquire a Page view conversion. (Page view CPA = Total cost / Page view)

Report types: dspCampaign, dspInventory, dspAudience, dspGeo

pageViewCVR
Type: Decimal

Description: The number of Page view conversions relative to the number of ad impressions. (Page view CVR = Page view / Impressions)

Report types: dspCampaign, dspInventory, dspAudience, dspGeo

pageViewClicks
Type: Integer

Description: The number of Page view conversions attributed to an ad click.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

pageViewValueAverage
Type: Decimal

Description: Average value associated with a Page view conversion. (Page view value average = Page view value sum / Page view)

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

pageViewValueSum
Type: Decimal

Description: Sum of Page view conversion values

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

pageViewViews
Type: Integer

Description: The number of Page view conversions attributed to an ad view.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

pageViews
Type: Integer

Description: The number of Page view conversions.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

paidSubscriptionSignupClicks
Type: Integer

Description: The number of paid subscriptions for sponsored products associated with a click on your ad.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

paidSubscriptionSignupRate
Type: Deciimal

Description: The ratio of how often customers signed up for a paid subscription for sponsored products when you ad was displayed. This is calculated as paid subscriptions divided by impressions.

Report types: dspCampaign, dspInventory, dspAudience

paidSubscriptionSignupViews
Type: Integer

Description: The number of paid subscriptions for sponsored products associated with ad impressions.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

paidSubscriptionSignups
Type: Integer

Description: The number of paid subscriptions for sponsored products associated with a click or view on your ad.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

parentAsin
Type: String

Description: The Amazon Standard Identification Number (ASIN) that is the parent of this ASIN.

Report types: dspProduct

peerSetSize
Type: String

Description: Range of brands included in a brand's peer set group.

Report types: benchmarks

percentOfPurchasesNewToBrand
Type: Decimal

Description: The percentage of attributed purchases by shoppers who had not purchased a product from the brand in the last 12 months. Percent of purchases new to brand = purchases (new to brand) / purchases.

Report types: benchmarks

percentOfPurchasesNewToBrandP25
Type: Decimal

Description: The percentage of attributed purchases by shoppers who had not purchased a product from the brand in the last 12 months. It shows the performance of the bottom 25% peer brands.

Report types: benchmarks

percentOfPurchasesNewToBrandP50
Type: Decimal

Description: The percentage of attributed purchases by shoppers who had not purchased a product from the brand in the last 12 months. It shows the performance of the median 50% of peer brands, where half of the peer brands performed above and half of the brands performed below the median.

Report types: benchmarks

percentOfPurchasesNewToBrandP75
Type: Decimal

Description: The percentage of attributed purchases by shoppers who had not purchased a product from the brand in the last 12 months. It excludes the performance of the top 25% peer brands.

Report types: benchmarks

placement
Type: String

Description: The name of the placement the campaign was run

Report types: dspInventory

placementClassification
Type: String

Description: The page location where an ad appeared.

Report types: spCampaigns, sbPlacement

placementSize
Type: Integer

Description: The dimensions of the placement in pixels. Only available when "site" is a dimension.

Report types: dspInventory

playTrailerRate
Type: Decimal

Description: The number of video trailer plays relative to the number of impressions. (Play trailer rate = Play trailers / Impressions)

Report types: dspCampaign, dspInventory, dspAudience

playTrailers
Type: Integer

Description: The number of times a video trailer was played for the featured product.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

playTrailersClicks
Type: Integer

Description: The number of video trailer plays attributed to ad click-throughs.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

playTrailersViews
Type: Integer

Description: The number of video trailer players attributed to ad impressions.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

portfolioId
Type: Integer

Description: The portfolio the campaign is associated with.

Report types: spTargeting, spSearchTerm, spPurchasedProduct, stCampaigns, stTargeting, spAdvertisedProduct

postalCode
Type: String

Description: Postal code.

Report types: dspGeo

productCategory
Type: String

Description: The category the product is associated with on Amazon.

Report types: sbPurchasedProduct, dspProduct

productGroup
Type: String

Description: A distinct product grouping distinguishing products like books from watches and video games from toys. Contains categories.

Report types: dspProduct

productName
Type: String

Description: The name of the product.

Report types: sbPurchasedProduct, dspProduct

productReviewPageViewBrandHalo
Type: Integer

Description: Number of times shoppers visited the product review page for a brand halo product, attributed to an ad view or click. Use Total PRPV to see all conversions for the brands' products.

Report types: dspProduct

productReviewPageViewBrandHaloClicks
Type: Integer

Description: Number of times shoppers visited the product review page for a brand halo product, attributed to an ad click. Use Total PRPV clicks to see all conversions for the brands' products.

Report types: dspProduct

productReviewPageViewBrandHaloViews
Type: Integer

Description: Number of times shoppers visited the product review page for a brand halo product, attributed to an ad view. Use Total PRPV views to see all conversions for the brands' products.

Report types: dspProduct

productReviewPageVisitRate
Type: Deciaml

Description: Rate of product review page visits for promoted products, relative to the number of ad impressions. (ATCR = ATC / Impressions) Use Total PRPVR to see all conversions for the brands' products.

Report types: dspCampaign, dspInventory, dspAudience

productReviewPageVisits
Type: Integer

Description: Number of times shoppers visited the product review page for a promoted product, attributed to an ad view or click. Use Total PRPV to see all conversions for the brands' products.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

productReviewPageVisitsClicks
Type: Integer

Description: Number of times shoppers visited the product review page for a promoted product, attributed to an ad click. Use Total PRPV clicks to see all conversions for the brands' products.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

productReviewPageVisitsViews
Type: Integer

Description: Number of times shoppers visited the product review page for a promoted product, attributed to an ad view. Use Total PRPV views to see all conversions for the brands' products.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

productSubCategory
Type: String

Description: A classification for the type of product being sold which determines its place in the Amazon retail catalog.

Report types: dspProduct

promptText
Type: String

Description: The AI-generated conversational text displayed with the ad that helps shoppers discover products by providing intelligent suggestions, answering questions, and surfacing relevant product information at critical decision points.

Report types: spPromptAdExtension

promotedAsin
Type: String

Description: The ASIN associated to an advertised product.

Report types: sdAdvertisedProduct, sdPurchasedProduct

promotedSku
Type: String

Description: The SKU being advertised. Not available for vendors.

Report types: sdAdvertisedProduct, sdPurchasedProduct

proposalId
Type: String

Description: A unique identifier for an order imported from the Amazon Order Management System (OMS).

Report types: dspCampaign

purchaseRate
Type: Decimal

Description: Rate of ad-attributed purchase events for promoted products, relative to ad impressions. (Purchase rate = Purchases / Impressions) Use Total purchase rate to see all conversions for the brands' products.

Report types: dspCampaign, dspInventory, dspAudience

purchasedAsin
Type: String

Description: The ASIN or retailer offer ID of the product that was purchased. This value may differ in format and length from a standard 10-character ASIN.

Report types: spPurchasedProduct, sbPurchasedProduct

purchases
Type: Integer

Description: Number of attributed conversion events occurring within 14 days of an ad click or view.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sbSearchTerm, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, stCampaigns, stTargeting, sbAds, dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience, sbAudiences, conversionPath

purchases14d
Type: Integer

Description: Number of attributed conversion events occurring within 14 days of an ad click. Sponsored Products only.

Report types: spCampaigns, spTargeting, spSearchTerm, spPurchasedProduct, spAdvertisedProduct, spGlobalAudiences, spPromptAdExtension

purchases1d
Type: Integer

Description: Number of attributed conversion events occurring within 1 day of an ad click.

Report types: spCampaigns, spTargeting, spSearchTerm, spPurchasedProduct, spAdvertisedProduct, spGlobalAudiences, spPromptAdExtension

purchases30d
Type: Integer

Description: Number of attributed conversion events occurring within 30 days of an ad click.

Report types: spCampaigns, spTargeting, spSearchTerm, spPurchasedProduct, spAdvertisedProduct, spGlobalAudiences, spPromptAdExtension

purchases7d
Type: Integer

Description: Number of attributed conversion events occurring within 7 days of an ad click.

Report types: spCampaigns, spTargeting, spSearchTerm, spPurchasedProduct, spAdvertisedProduct, spGlobalAudiences, spPromptAdExtension

purchasesBrandHalo
Type: Integer

Description: Number of times any quantity of a brand halo product was included in a purchase event, attributed to an ad view or click. Purchase events include new Subscribe & Save subscriptions and video rentals. Use Total purchases to see all conversions for the brands' products.

Report types: dspProduct

purchasesBrandHaloClicks
Type: Integer

Description: Number of times any quantity of a brand halo product was included in a purchase event, attributed to an ad click. Purchase events include new Subscribe & Save subscriptions and video rentals. Use Total purchases clicks to see all conversions for the brands' products.

Report types: dspProduct

purchasesBrandHaloViews
Type: Integer

Description: Number of times any quantity of a brand halo product was included in a purchase event, attributed to an ad view. Purchase events include new Subscribe & Save subscriptions and video rentals. Use Total purchases views to see all conversions for the brands' products.

Report types: dspProduct

purchasesClicks
Type: Integer

Description: Number of attributed conversion events occurring within 14 days of an ad click.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sbSearchTerm, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, stCampaigns, stTargeting, sbAds, dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

purchasesClicksRate
Type: Decimal

Description: Rate of click-attributed purchases for promoted products relative to the number of ad impressions. (Purchase Rate Clicks = Click-attributed purchases / Impressions) Use Total Purchase Click Rate to see all conversions for the brands' products.

Report types: dspAudience

purchasesOtherSku14d
Type: Integer

Description: Number of attributed conversion events occurring within 14 days of an ad click where the SKU purchased was different that the advertised SKU.

Report types: spPurchasedProduct, spPromptAdExtension

purchasesOtherSku1d
Type: Integer

Description: Number of attributed conversion events occurring within 1 day of an ad click where the SKU purchased was different that the advertised SKU.

Report types: spPurchasedProduct, spPromptAdExtension

purchasesOtherSku30d
Type: Integer

Description: Number of attributed conversion events occurring within 30 days of an ad click where the SKU purchased was different that the advertised SKU.

Report types: spPurchasedProduct, spPromptAdExtension

purchasesOtherSku7d
Type: Integer

Description: Number of attributed conversion events occurring within 7 days of an ad click where the SKU purchased was different that the advertised SKU.

Report types: spPurchasedProduct, spPromptAdExtension

purchasesPromoted
Type: Integer

Description: Number of attributed conversion events occurring within 14 days of ad click or view where the purchased SKU was the same as the SKU advertised. Same as purchasesSameSku14d.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sbAds

purchasesPromotedClicks
Type: Integer

Description: Number of attributed conversion events occurring within 14 days of ad click where the purchased SKU was the same as the SKU advertised.

Report types: sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct

purchasesSameSku14d
Type: Integer

Description: Number of attributed conversion events occurring within 14 days of ad click where the purchased SKU was the same as the SKU advertised. Sponsored Products only. Same as puchasesPromoted.

Report types: spCampaigns, spTargeting, spSearchTerm, spAdvertisedProduct, spGlobalAudiences, spPromptAdExtension

purchasesSameSku1d
Type: Integer

Description: Number of attributed conversion events occurring within 1 day of ad click where the purchased SKU was the same as the SKU advertised.

Report types: spCampaigns, spTargeting, spSearchTerm, spAdvertisedProduct, spGlobalAudiences, spPromptAdExtension

purchasesSameSku30d
Type: Integer

Description: Number of attributed conversion events occurring within 30 days of ad click where the purchased SKU was the same as the SKU advertised.

Report types: spCampaigns, spTargeting, spSearchTerm, spAdvertisedProduct, spGlobalAudiences, spPromptAdExtension

purchasesSameSku7d
Type: Integer

Description: Number of attributed conversion events occurring within 7 days of ad click where the purchased SKU was the same as the SKU advertised.

Report types: spCampaigns, spTargeting, spSearchTerm, spAdvertisedProduct, spGlobalAudiences, spPromptAdExtension

purchasesViews
Type: Integer

Description: Number of attributed conversion events occurring within 14 days of an ad view.

Report types: stCampaigns, stTargeting, dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

qualifiedBorrows
Type: Integer

Description: Number of Kindle Unlimited users who have downloaded the book due to ad exposure, during the attribution window, and have read a percent of the book within the window, triggering a royalty payment. Relevant to book advertisers only.

Report types: spCampaigns, sbCampaigns, sbAdGroups, sbPlacement, spTargeting, sbTargeting, spSearchTerm, sbSearchTerm, spPurchasedProduct, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, sdPurchasedProduct, sbAds, spAdvertisedProduct

qualifiedBorrowsFromClicks
Type: Integer

Description: Number of Kindle Unlimited users who have downloaded the book due to ad exposure, during the attribution window, and have read a percent of the book within the window, triggering a royalty payment. Relevant to book advertisers only.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sbSearchTerm, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, sdPurchasedProduct, sbAds

qualifiedBorrowsFromViews
Type: Integer

Description: Number of Kindle Unlimited users who have downloaded the book due to ad exposure, during the attribution window, and have read a percent of the book within the window, triggering a royalty payment. Relevant to book advertisers only.

Report types: sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, sdPurchasedProduct

reach
Type: Integer

Description: The number of unique users exposed to ads, counted either daily or over the last 6 months, depending on the selected time unit (Daily vs. Summary)

Report types: stCampaigns, dspCampaign, dspReachFrequency

region
Type: String

Description: State or region.

Report types: dspGeo

rentalRate
Type: Decimal

Description: The number of video rentals relative to the number of impressions. (Rental rate = Rentals / Impressions)

Report types: dspCampaign, dspInventory, dspAudience

rentals
Type: Integer

Description: The number of times a video was rented for the featured product.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

rentalsClicks
Type: Integer

Description: The number of video rentals attributed to ad click-throughs.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

rentalsViews
Type: Integer

Description: The number of video rentals attributed to ad impressions.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

reportGranularity
Type: String

Description: Report granularity.

Report types: dspProduct

roas
Type: Decimal

Description: Return on ad spend.

Report types: stCampaigns, stTargeting, dspCampaign, dspInventory

roasClicks14d
Type: Decimal

Description: Return on ad spend based on purchases made within 14 days of an ad click.

Report types: spTargeting, spSearchTerm, spAdvertisedProduct, spPromptAdExtension

roasClicks7d
Type: Decimal

Description: Return on ad spend based on purchases made within 7 days of an ad click.

Report types: spTargeting, spSearchTerm, spAdvertisedProduct, spPromptAdExtension

royaltyQualifiedBorrows
Type: Decimal

Description: Estimated royalty payment attributed to Kindle Unlimited users downloading the book due to ad exposure, during the attribution window, and have read a percent of the book within the window, triggering a royalty payment. Relevant to book advertisers only.

Report types: spCampaigns, sbCampaigns, sbAdGroups, sbPlacement, spTargeting, sbTargeting, spSearchTerm, sbSearchTerm, spPurchasedProduct, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, sdPurchasedProduct, sbAds, spAdvertisedProduct

royaltyQualifiedBorrowsFromClicks
Type: Decimal

Description: Estimated royalty payment attributed to Kindle Unlimited users who clicked on the ad, downloaded the book due to ad exposure, during the attribution window, and have read a percent of the book within the window, triggering a royalty payment. Relevant to book advertisers only.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sbSearchTerm, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, sdPurchasedProduct, sbAds

royaltyQualifiedBorrowsFromViews
Type: Decimal

Description: Estimated royalty payment attributed to Kindle Unlimited users who viewed the ad, downloaded the book due to ad exposure, during the attribution window, and have read a percent of the book within the window, triggering a royalty payment. Relevant to book advertisers only.

Report types: sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, sdPurchasedProduct

sales
Type: Decimal

Description: Total value of sales occurring within 14 days of an ad click or view.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sbSearchTerm, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, stCampaigns, stTargeting, sbAds, dspCampaign, dspInventory, sbAudiences, dspGeo, dspProduct, dspTech, conversionPath

sales14d
Type: Decimal

Description: Total value of sales occurring within 14 days of an ad click. Includes sales attributed to both clicks and views for vCPM campaigns, but only sales attributed to clicks for CPC campaigns.

Report types: spCampaigns, spTargeting, spSearchTerm, spPurchasedProduct, sbPurchasedProduct, spAdvertisedProduct, spGlobalAudiences, spPromptAdExtension

sales1d
Type: Decimal

Description: Total value of sales occurring within 1 day of an ad click.

Report types: spCampaigns, spTargeting, spSearchTerm, spPurchasedProduct, spAdvertisedProduct, spGlobalAudiences, spPromptAdExtension

sales30d
Type: Decimal

Description: Total value of sales occurring within 30 days of an ad click.

Report types: spCampaigns, spTargeting, spSearchTerm, spPurchasedProduct, spAdvertisedProduct, spGlobalAudiences, spPromptAdExtension

sales7d
Type: Decimal

Description: Total value of sales occurring within 7 days of an ad click.

Report types: spCampaigns, spTargeting, spSearchTerm, spPurchasedProduct, spAdvertisedProduct, spGlobalAudiences, spPromptAdExtension

salesBrandHalo
Type: Decimal

Description: For Sponsored Display vCPM campaigns, the total value of sales occurring within 14 days of an ad click or view where the purchased SKU was different from the SKU advertised.

Report types: sdPurchasedProduct, dspProduct

salesBrandHaloClicks
Type: Decimal

Description: Total value of sales occurring within 14 days of an ad click where the purchased SKU was different from the SKU advertised.

Report types: sdPurchasedProduct

newToBrandSalesBrandHalo
Type: Integer

Description: The total new-to-brand sales of brand halo products purchased by customers on Amazon after exposure to an ad.

Report types: dspProduct

salesClicks
Type: Decimal

Description: Total value of sales occurring within 14 days of an ad click.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sbSearchTerm, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, stCampaigns, stTargeting, sbAds, dspProduct, dspGeo, sbAudiences

salesClicks14d
Type: Decimal

Description: Total value of sales occurring within 14 days of an ad click.

Report types: sbPurchasedProduct

salesCurrencyCode
Type: String

Description: The currency code of the marketplace of the purchase event.

Report types: conversionPath

salesOtherSku14d
Type: Decimal

Description: Total value of sales occurring within 14 days of an ad click where the purchased SKU was different from the SKU advertised.

Report types: spPurchasedProduct, spPromptAdExtension

salesOtherSku1d
Type: Decimal

Description: Total value of sales occurring within 1 day of an ad click where the purchased SKU was different from the SKU advertised.

Report types: spPurchasedProduct, spPromptAdExtension

salesOtherSku30d
Type: Decimal

Description: Total value of sales occurring within 30 days of an ad click where the purchased SKU was different from the SKU advertised.

Report types: spPurchasedProduct, spPromptAdExtension

salesOtherSku7d
Type: Decimal

Description: Total value of sales occurring within 7 days of an ad click where the purchased SKU was different from the SKU advertised.

Report types: spTargeting, spSearchTerm, spPurchasedProduct, spAdvertisedProduct, spPromptAdExtension

salesPromoted
Type: Decimal

Description: Total value of sales occurring within 14 days of ad click or view where the purchased SKU was the same as the SKU advertised. Same as attributedSales14dSameSKU.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sbAds, dspProduct

salesPromotedClicks
Type: Decimal

Description: Total value of sales occurring within 14 days of ad click where the purchased SKU was the same as the SKU advertised.

Report types: sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, dspProduct, dspGeo

salesViews
Type: Decimal

Description: Total value of sales occurring within 14 days of an ad view.

Report types: stCampaigns, stTargeting

search
Type: Integer

Description: The number of Search conversions.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

searchCPA
Type: Decimal

Description: The average cost to acquire a Search conversion. (Search CPA = Total cost / Search)

Report types: dspCampaign, dspInventory, dspAudience, dspGeo

searchCVR
Type: Decimal

Description: The number of Search conversions relative to the number of ad impressions. (Search CVR = Search / Impressions)

Report types: dspCampaign, dspInventory, dspAudience, dspGeo

searchClicks
Type: Integer

Description: The number of Search conversions attributed to an ad click.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

searchTerm
Type: String

Description: The search term used by the customer. Same as query.

Report types: spSearchTerm, sbSearchTerm

searchValueAverage
Type: Decimal

Description: Average value associated with a Search conversion. (Search value average = Search value sum / Search)

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

searchValueSum
Type: Decimal

Description: Sum of Search conversion values

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

searchViews
Type: Integer

Description: The number of Search conversions attributed to an ad view.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

segmentClassCode
Type: String

Description: The segment's class, for example behavioral or user agent.

Report types: dspAudience, spGlobalAudiences

segmentId
Type: String

Description: A unique identifier assigned to an audience segment.

Report types: dspAudience

segmentMarketplaceId
Type: String

Description: A unique identifier assigned to the marketplace of the audience segment.

Report types: dspAudience

segmentName
Type: String

Description: The name of the audience segment.

Report types: dspAudience, spGlobalAudiences, sbAudiences

segmentSource
Type: String

Description: The segment's source, for example AAX.

Report types: dspAudience

segmentType
Type: String

Description: The type of segment, for example remarketing.

Report types: dspAudience

signUp
Type: Integer

Description: Number of Sign-up conversions occurring off Amazon, attributed to an ad view or click.

Report types: dspCampaign, dspGeo, dspAudience, dspInventory, dspTech

signUpCPA
Type: Decimal

Description: The average cost to acquire a Sign-up conversion off Amazon. (Total cost / Sign-up)

Report types: dspCampaign, dspInventory, dspAudience

signUpCVR
Type: Decimal

Description: Number of Sign-up conversions occurring off Amazon relative to the number of ad impressions. (Sign-up/ Impressions)

Report types: dspCampaign, dspInventory, dspAudience

signUpClicks
Type: Integer

Description: Number of Sign-up conversions occurring off Amazon, attributed to an ad click.

Report types: dspCampaign, dspGeo, dspAudience, dspInventory, dspTech

signUpValueAverage
Type: Decimal

Description: Average value associated with a Sign-up conversion. (Sign-up value average = Sign-up value sum / Sign-up)

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

signUpValueSum
Type: Decimal

Description: Sum of Sign-up conversion values

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

signUpViews
Type: Integer

Description: Number of Sign-up conversions occurring off Amazon, attributed to an ad view.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

simplifiedPath
Type: String

Description: A Conversion Path is a sequence of ad touchpoints on a customer's path to a given conversion event (e.g., purchases, detail page views). A simplified path collapses duplicate ad-touchpoints to the first ad-touchpoint interaction in the path.

Report types: conversionPath

site
Type: String

Description: The site or group of sites the campaign ran on.

Report types: dspInventory

skillInvocation
Type: Integer

Description: The number of times shoppers launched a promoted Alexa skill, attributed to an ad view or click. This can include tap, touch, and voice invocations.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

skillInvocationClicks
Type: Integer

Description: The number of times shoppers launched a promoted Alexa skill, attributed to an ad click. This can include tap, touch, and voice invocations.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

skillInvocationRate
Type: Decimal

Description: Rate of Skill invocation conversions relative to the number of impressions. (Skill invocation rate = Skill invocations / Impressions)

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

skillInvocationViews
Type: Integer

Description: The number of times shoppers launched a promoted Alexa skill, attributed to an ad view. This can include tap, touch, and voice invocations.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

spend
Type: Decimal

Description: Total cost of ad clicks.

Report types: spCampaigns, spAdvertisedProduct, spGlobalAudiences, sbAudiences, spPromptAdExtension

sponsoredBrandsDisplayFrequency
Type: Decimal

Description: Average number of Sponsored Brands display occurrences in the simplified path.

Report types: conversionPath

sponsoredBrandsVideoFrequency
Type: Decimal

Description: Average number of Sponsored Brands video occurrences in the simplified path.

Report types: conversionPath

sponsoredDisplayDisplayFrequency
Type: Decimal

Description: Average number of Sponsored Display display occurrences in the simplified path.

Report types: conversionPath

sponsoredDisplayFrequency
Type: Decimal

Description: Average number of Sponsored Display occurrences in the simplified path.

Report types: conversionPath

sponsoredDisplayOnlineVideoFrequency
Type: Decimal

Description: Average number of Sponsored Display video occurrences in the simplified path.

Report types: conversionPath

sponsoredProductsFrequency
Type: Decimal

Description: Average number of Sponsored Products occurrences in the simplified path.

Report types: conversionPath

sponsoredTvStreamingTvFrequency
Type: Decimal

Description: Average number of Sponsored TV streaming TV occurrences in the simplified path.

Report types: conversionPath

startDate
Type: String

Description: Start date of summary period for a report in the format YYYY-MM-DD.

Report types: spCampaigns, sbCampaigns, sbAdGroups, sbPlacement, spTargeting, sbTargeting, spSearchTerm, sbSearchTerm, spPurchasedProduct, sbPurchasedProduct, sdCampaigns, sdAdGroups, sdAdvertisedProduct, sdPurchasedProduct, stCampaigns, stTargeting, spGrossandInvalids, sbGrossandInvalids, sdGrossandInvalids, sbAds, spAdvertisedProduct, spGlobalAudiences, sbAudiences,dspBidAdjustment, conversionPath, benchmarks, spPromptAdExtension

subscribe
Type: Integer

Description: Number of Subscribe conversions occurring off Amazon, attributed to an ad view or click.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

subscribeCPA
Type: Decimal

Description: Average cost to acquire a Subscribe conversion off Amazon. (Total cost / Subscribe)

Report types: dspCampaign, dspInventory, dspAudience

subscribeCVR
Type: Decimal

Description: Number of Subscribe conversions occurring off Amazon, relative to the number of ad impressions. (Subscribe / Impressions)

Report types: dspCampaign, dspInventory, dspAudience

subscribeClicks
Type: Integer

Description: Number of Subscribe conversions occurring off Amazon, attributed to an ad click.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

subscribeValueAverage
Type: Decimal

Description: Average value associated with a Subscribe conversion. (Subscribe value average = Subscribe value sum / Subscribe)

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

subscribeValueSum
Type: Decimal

Description: Sum of Subscribe conversion values

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

subscribeViews
Type: Integer

Description: Number of Subscribe conversions occurring off Amazon, attributed to an ad view.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

subscriptionSignupClicks
Type: Integer

Description: The number of free trial and paid subscriptions for sponsored products associated with a click on your ad.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

subscriptionSignupRate
Type: Decimal

Description: The ratio of how often customers signed up for a free trial or paid subscription for sponsored products when you ad was displayed. This is calculated as free trials and paid subscriptions divided by impressions.

Report types: dspCampaign, dspInventory, dspAudience

subscriptionSignupViews
Type: Integer

Description: The number of free trial and paid subscriptions for sponsored products associated with ad impressions.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

subscriptionSignups
Type: Integer

Description: The number of free trial and paid subscriptions for sponsored products associated with a click or view on your ad.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

supplyCost
Type: Decimal

Description: The total amount of money spent on media supply.

Report types: dspCampaign, dspInventory, dspAudience

supplySource
Type: String

Description: The inventory the campaign ran on, for example real-time bidding exchanges or Amazon-owned sites.

Report types: dspInventory, dspAudioAndVideo, dspReachFrequency

supplySourceId
Type: Integer

Description: The ID associated to the inventory the campaign ran on.

Report types: dspReachFrequency

targetDemographic
Type: String

Description: The Nielsen demographic segment the advertiser is transacting on

Report types: dspCampaign

targeting
Type: String

Description: A string representation of the expression object used in the targeting clause.

Report types: spTargeting, spSearchTerm

targetingExpression
Type: String

Description: A string representation of the expression object used in the targeting clause.

Report types: sbTargeting, sdTargeting

targetingId
Type: Integer

Description: The identifier of the targeting expression.

Report types: sbTargeting, sdTargeting

targetingMethod
Type: String

Description: The targeting settings applied to the campaign. Examples include segments, content categories, and untargeted if no settings were applied.

Report types: dspAudience

targetingText
Type: String

Description: The text used in the targeting expression.

Report types: sbTargeting, sdTargeting, stTargeting

targetingType
Type: String

Description: The type of targeting used in the expression.

Report types: sbTargeting

topOfSearchImpressionShare
Type: Decimal

Description: The percentage of top-of-search impressions earned out of all the top-of-search impressions that were eligible for a given date range. Various factors determine the eligibility for an impression including campaign status and targeting status.

Report types: spCampaigns, sbCampaigns, sbTargeting

totalAddToCart
Type: Integer

Description: Number of times shoppers added the brands' products to their cart, attributed to an ad view or click.

Report types: dspCampaign, dspInventory, dspProduct, dspGeo

totalAddToCartClicks
Type: Integer

Description: Number of times shoppers added the brands' products to their cart, attributed to an ad click.

Report types: dspCampaign, dspInventory, dspProduct, dspGeo

totalAddToCartRate
Type: Decimal

Description: Rate of Add to Cart conversions for the brands' products relative to the number of ad impressions. (Total ATCR = Total ATC / Impressions)

Report types: dspCampaign, dspInventory

totalAddToCartViews
Type: Integer

Description: Number of times shoppers added the brands' products to their cart, attributed to an ad view.

Report types: dspCampaign, dspInventory, dspProduct, dspGeo

totalAddToList
Type: Integer

Description: Number of times shoppers added the brands' products to a wish list, gift list, or registry, attributed to an ad view or click.

Report types: dspCampaign, dspInventory, dspProduct, dspGeo

totalAddToListClicks
Type: Integer

Description: Number of times shoppers added the brands' products to a wish list, gift list, or registry, attributed to an ad click.

Report types: dspCampaign, dspInventory, dspProduct, dspGeo

totalAddToListRate
Type: Decimal

Description: Rate of Add to List conversions for the brands' products relative to the number of impressions. (ATLR = ATL / Impressions)

Report types: dspCampaign, dspInventory

totalAddToListViews
Type: Integer

Description: Number of times shoppers added the brands' products to a wish list, gift list or registry, attributed to an ad view.

Report types: dspCampaign, dspInventory, dspProduct, dspGeo

totalCost
Type: Decimal

Description: The total amount of money spent on running the campaign not including 3P fees paid by the agency.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

totalDetailPageView
Type: Integer

Description: Number of detail page views for all the brands and products attributed to an ad view or click.

Report types: dspCampaign, dspInventory, dspProduct, dspGeo

totalDetailPageViewClicks
Type: Integer

Description: Number of detail page views for all the brands and products attributed to an ad click.

Report types: dspCampaign, dspInventory, dspProduct, dspGeo

totalDetailPageViewRate
Type: Decimal

Description: Detail page view rate for the brands’ products, relative to the number of ad impressions. (Total DPV / Impressions = Total DPVR)

Report types: dspCampaign, dspInventory

totalDetailPageViewViews
Type: Integer

Description: Number of detail page views for all the brands' products, attributed to an ad view.

Report types: dspCampaign, dspInventory, dspProduct, dspGeo

totalECPAddToCart
Type: Decimal

Description: Effective (average) cost to acquire an Add to Cart conversion for the brands' products. (Total eCPATC = Total cost / Total ATC)

Report types: dspCampaign, dspInventory

totalECPAddToList
Type: Decimal

Description: Effective (average) cost to acquire an Add to List conversion for the brands' products. (Total eCPATL = Total cost / Total ATL)

Report types: dspCampaign, dspInventory

totalECPDetailPageView
Type: Decimal

Description: Effective (average) cost to acquire a detail page view for a product in your brand. (Total eCPDPV = Total cost / Total DPV)

Report types: dspCampaign, dspInventory

totalECPP
Type: Decimal

Description: Effective (average) cost to acquire a purchase conversion for the brands' products. (Total eCPP = Total cost / Total purchases)

Report types: dspCampaign, dspInventory

totalECPProductReviewPageVisit
Type: Decimal

Description: Effective (average) cost to acquire a product review page conversion for the brands' products. (Total eCPPRPV = Total cost / Total PRPV)

Report types: dspCampaign, dspInventory

totalECPSubscribeAndSave
Type: Decimal

Description: Effective (average) cost to acquire a Subscribe & Save subscription for the brands' products. (Total eCPSnSS = Total cost / Total SnSS)

Report types: dspCampaign, dspInventory

totalERPM
Type: Decimal

Description: Effective (average) revenue for the brands’ products generated per thousand impressions. (Total eRPM = Sales / (Impressions / 1000))

Report types: dspCampaign, dspInventory

totalFee
Type: Decimal

Description: The sum of all fees.

Report types: dspCampaign, dspInventory

totalNewToBrandDPVClicks
Type: Integer

Description: Number of new-to-brand detail page views for all the brands' products, attributed to an ad click.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

totalNewToBrandDPVRate
Type: Decimal

Description: The new-to-brand detail page view rate for the brands' products, relative to the number of ad impressions. (Total NTB - DPV / Impressions = Total DPVR)

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

totalNewToBrandDPVViews
Type: Integer

Description: Number of new-to-brand detail page views for all the brands' products, attributed to an ad view.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

totalNewToBrandDPVs
Type: Integer

Description: Number of new-to-brand detail page views for all the brands' products, attributed to an ad view or click.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

totalNewToBrandECPDetailPageView
Type: Decimal

Description: Effective total cost for new-to-brand detail page view, calculated by cost divided by new-to-brand detail page view

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

totalNewToBrandECPP
Type: Decimal

Description: Effective (average) cost to acquire a new-to-brand purchase conversion for the brands' products. (Total new-to-brand eCPP = Total cost / Total new-to-brand purchases)

Report types: dspCampaign, dspInventory

totalNewToBrandERPM
Type: Decimal

Description: Effective (average) revenue generated per thousand impressions from the brands’ products purchased by new-to-brand shoppers. (Total NTB eRPM = Total NTB Sales / (Impressions / 1000))

Report types: dspCampaign, dspInventory

totalNewToBrandPurchaseRate
Type: Decimal

Description: Rate of new-to-brand purchase conversions for the brands' products relative to the number of ad impressions. (Total new-to-brand purchase rate = Total new-to-brand purchases / Impressions)

Report types: dspCampaign, dspInventory

totalNewToBrandPurchases
Type: Integer

Description: Number of new-to-brand purchases for the brands’ products, attributed to an ad view or click. Shoppers are "new to brand" if they have not purchased from the brand in the last 365 days.

Report types: dspCampaign, dspInventory, dspProduct, dspGeo

totalNewToBrandPurchasesClicks
Type: Integer

Description: Number of new-to-brand purchases for the brands’ products, attributed to an ad click. Shoppers are "new to brand" if they have not purchased from the brand in the last 365 days.

Report types: dspCampaign, dspInventory, dspProduct, dspGeo

totalNewToBrandPurchasesPercentage
Type: Decimal

Description: Rate of new-to-brand purchase conversions for the brands' products relative to the number of ad impressions. (Total new-to-brand purchase rate = Total new-to-brand purchases / Impressions)

Report types: dspCampaign, dspProduct

totalNewToBrandPurchasesViews
Type: Integer

Description: Number of new-to-brand purchases for the brands’ products, attributed to an ad view. Shoppers are "new to brand" if they have not purchased from the brand in the last 365 days.

Report types: dspCampaign, dspInventory, dspProduct, dspGeo

totalNewToBrandROAS
Type: Decimal

Description: Return on advertising spend for new-to-brand purchases, measured as ad-attributed new-to-brand sales for the brands' products per local currency unit of ad spend. (Total new-to-brand ROAS = Total new to brand product sales / Total cost)

Report types: dspCampaign, dspInventory

totalNewToBrandSales
Type: Decimal

Description: Sales (in local currency) of the brands’ products purchased by new-to-brand shoppers, attributed to an ad view or click. Shoppers are "new to brand" if they have not purchased from the brand in the last 365 days.

Report types: dspCampaign, dspInventory, dspGeo, dspProduct

totalNewToBrandUnitsSold
Type: Integer

Description: Units of the brands' products purchased by shoppers who were new-to-brand, attributed to an ad view or click. A single new-to-brand purchase event can include multiple sold units.

Report types: dspCampaign, dspInventory, dspProduct, dspGeo

totalProductReviewPageVisitRate
Type: Decimal

Description: Rate of product review page visits for the brands' products, relative to the number of ad impressions. (Total ATCR = Total ATC / Impressions)

Report types: dspCampaign, dspInventory

totalProductReviewPageVisits
Type: Integer

Description: Number of times shoppers visited a product review page for the brands' products, attributed to an ad view or click.

Report types: dspCampaign, dspInventory, dspProduct, dspGeo

totalProductReviewPageVisitsClicks
Type: Integer

Description: Number of times shoppers visited a product review page for the brands' products, attributed to an ad click.

Report types: dspCampaign, dspInventory, dspProduct, dspGeo

totalProductReviewPageVisitsViews
Type: Integer

Description: Number of times shoppers visited a product review page for the brands' products, attributed to an ad view.

Report types: dspCampaign, dspInventory, dspProduct, dspGeo

totalPurchaseRate
Type: Decimal

Description: Rate of ad-attributed purchase events for the brands' products relative to ad impressions. (Total purchase rate = Total purchases / Impressions)

Report types: dspCampaign, dspInventory

totalPurchases
Type: Integer

Description: Number of times any quantity of a brand product was included in a purchase event, attributed to an ad view or click. Purchase events include new Subscribe & Save subscriptions and video rentals.

Report types: dspCampaign, dspInventory, dspProduct, dspGeo

totalPurchasesClicks
Type: Integer

Description: Number of times any quantity of a brand product was included in a purchase event, attributed to an ad click. Purchase events include new Subscribe & Save subscriptions and video rentals.

Report types: dspCampaign, dspInventory, dspProduct, dspGeo

totalPurchasesViews
Type: Integer

Description: Number of times any quantity of a brand product was included in a purchase event, attributed to an ad view. Purchase events include new Subscribe & Save subscriptions and video rentals.

Report types: dspCampaign, dspInventory, dspProduct, dspGeo

totalROAS
Type: Decimal

Description: Return on ad spend, measured as ad-attributed sales for the brands’ products per local currency unit of ad spend. (Total ROAS = Total product sales / Total cost)

Report types: dspCampaign, dspInventory

totalSales
Type: Decimal

Description: Sales (in local currency) of the brands’ products, attributed to an ad view or click.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspProduct

totalSubscribeAndSave
Type: Integer

Description: Number of new Subscribe & Save subscriptions for the brands and products, attributed to an ad view or click. This does not include replenishment subscription orders.

Report types: dspCampaign, dspInventory, dspProduct, dspGeo

totalSubscribeAndSaveClicks
Type: Integer

Description: Number of new Subscribe & Save subscriptions for the brands and products, attributed to an ad click. This does not include replenishment subscription orders.

Report types: dspCampaign, dspInventory, dspProduct, dspGeo

totalSubscribeAndSaveRate
Type: Decimal

Description: Rate of ad-attributed Subscribe & Save conversions for the brands’ products relative to ad impressions. (Total SnSSR = Total SnSS / Impressions)

Report types: dspCampaign, dspInventory

totalSubscribeAndSaveViews
Type: Integer

Description: Number of new Subscribe & Save subscriptions for the brands and products, attributed to an ad view. This does not include replenishment subscription orders.

Report types: dspCampaign, dspInventory, dspProduct, dspGeo

totalUnitsSold
Type: Integer

Description: Units of the brands' products purchased, attributed to an ad view or click. A single purchase event can include multiple sold units.

Report types: dspCampaign, dspInventory, dspProduct, dspGeo

unitsSold
Type: Integer

Description: Number of attributed units sold within 14 days of an ad click or view.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sbSearchTerm, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, stCampaigns, stTargeting, sbAds, dspCampaign, dspInventory, dspProduct, dspGeo, sbAudiences, dspTech

unitsSold14d
Type: Integer

Description: Number of attributed units sold within 14 days of an click or view. Only valid for Sponsored Brands version 3 campaigns, not Sponsored Brands video or multi-ad group (version 4) campaigns. Includes sales attributed to both clicks and views for vCPM campaigns, but only sales attributed to clicks for CPC campaigns.

Report types: sbPurchasedProduct

unitsSoldBrandHalo
Type: Integer

Description: For Sponsored Display vCPM campaigns, the total number of units ordered within 14 days of an ad click or view where the purchased SKU was different from the SKU advertised. For CPC campaigns, this value is equal to attributedUnitsOrdered14dOtherSKU.

Report types: sdPurchasedProduct, dspProduct

unitsSoldBrandHaloClicks
Type: Integer

Description: Total number of units ordered within 14 days of an ad click where the purchased SKU was different from the SKU advertised.

Report types: sdPurchasedProduct

unitsSoldClicks
Type: Integer

Description: Number of attributed units sold within 14 days of an ad click.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, stCampaigns, stTargeting, sbAds, dspProduct, dspGeo, sbAudiences

unitsSoldClicks14d
Type: Integer

Description: Total number of units sold within 14 days of an ad click.

Report types: spCampaigns, spTargeting, spSearchTerm, spPurchasedProduct, sbPurchasedProduct, spAdvertisedProduct, spGlobalAudiences, spPromptAdExtension

unitsSoldClicks1d
Type: Integer

Description: Total number of units ordered within 1 day of an ad click.

Report types: spCampaigns, spTargeting, spSearchTerm, spPurchasedProduct, spAdvertisedProduct, spGlobalAudiences, spPromptAdExtension

unitsSoldClicks30d
Type: Integer

Description: Total number of units ordered within 30 days of an ad click.

Report types: spCampaigns, spTargeting, spSearchTerm, spPurchasedProduct, spAdvertisedProduct, spGlobalAudiences, spPromptAdExtension

unitsSoldClicks7d
Type: Integer

Description: Total number of units ordered within 7 days of an ad click.

Report types: spCampaigns, spTargeting, spSearchTerm, spPurchasedProduct, spAdvertisedProduct, spGlobalAudiences, spPromptAdExtension

unitsSoldOtherSku14d
Type: Integer

Description: Total number of units ordered within 14 days of an ad click where the purchased SKU was different from the SKU advertised.

Report types: spPurchasedProduct, spPromptAdExtension

unitsSoldOtherSku1d
Type: Integer

Description: Total number of units ordered within 1 day of an ad click where the purchased SKU was different from the SKU advertised.

Report types: spPurchasedProduct, spPromptAdExtension

unitsSoldOtherSku30d
Type: Integer

Description: Total number of units ordered within 30 days of an ad click where the purchased SKU was different from the SKU advertised.

Report types: spPurchasedProduct, spPromptAdExtension

unitsSoldOtherSku7d
Type: Integer

Description: Total number of units ordered within 7 days of an ad click where the purchased SKU was different from the SKU advertised.

Report types: spTargeting, spSearchTerm, spPurchasedProduct, spAdvertisedProduct, spPromptAdExtension

unitsSoldPromotedClicks
Type: Integer

Description: Units of promoted products purchased, attributed to an ad click. A single click-attributed purchase event can include multiple sold units. Use Total Units Sold Clicks to see all conversions for the brands' products.

Report types: dspProduct, dspGeo

unitsSoldSameSku14d
Type: Integer

Description: Total number of units ordered within 14 days of ad click where the purchased SKU was the same as the SKU advertised.

Report types: spCampaigns, spTargeting, spSearchTerm, spAdvertisedProduct, spGlobalAudiences, spPromptAdExtension

unitsSoldSameSku1d
Type: Integer

Description: Total number of units ordered within 1 day of ad click where the purchased SKU was the same as the SKU advertised.

Report types: spCampaigns, spTargeting, spSearchTerm, spAdvertisedProduct, spGlobalAudiences, spPromptAdExtension

unitsSoldSameSku30d
Type: Integer

Description: Total number of units ordered within 30 days of ad click where the purchased SKU was the same as the SKU advertised.

Report types: spCampaigns, spTargeting, spSearchTerm, spAdvertisedProduct, spGlobalAudiences, spPromptAdExtension

unitsSoldSameSku7d
Type: Integer

Description: Total number of units ordered within 7 days of ad click where the purchased SKU was the same as the SKU advertised.

Report types: spCampaigns, spTargeting, spSearchTerm, spAdvertisedProduct, spGlobalAudiences, spPromptAdExtension

unitsSoldViews
Type: Integer

Description: Number of attributed units sold within 14 days of an ad view.

Report types: stCampaigns, stTargeting

video5SecondViewRate
Type: Decimal

Description: The percentage of impressions where the customer watched the complete video or 5 seconds of the video (whichever is shorter). Sponsored Brands video-only metric.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sbSearchTerm, sbAds

video5SecondViews
Type: Integer

Description: The number of impressions where the customer watched the complete video or 5 seconds (whichever is shorter). Sponsored Brands video-only metric.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sbSearchTerm, sbAds

videoAdClicks
Type: Integer

Description: The number of times a video ad was clicked excluding clicks to the navigation (e.g. Play or Pause buttons).

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

videoAdComplete
Type: Integer

Description: The number of times a video ad played to completion. If rewind occurred, completion was calculated on the total percentage of unduplicated video viewed.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

videoAdCompletionRate
Type: Integer

Description: The number of video completions relative to the number of video starts. (Video completion rate = Video complete / Video start)

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

videoAdCreativeViews
Type: Integer

Description: The number of times a portion of a video was seen.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

videoAdEndStateClicks
Type: Integer

Description: The number of ad clicks after a video ends.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

videoAdFirstQuartile
Type: Integer

Description: The number of times at least 25% of a video ad played. If rewind occurred, percent complete was calculated on the total percentage of unduplicated video viewed.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

videoAdImpressions
Type: Integer

Description: The number of times a video was served.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

videoAdMidpoint
Type: Integer

Description: The number of times at least 50% of a video ad played. If rewind occurred, percent complete was calculated on the total percentage of unduplicated video viewed.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

videoAdMute
Type: Integer

Description: The number of times a user muted the video ad.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

videoAdPause
Type: Integer

Description: The number of times a user paused the video ad.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

videoAdReplays
Type: Integer

Description: The number of times a video was replayed.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

videoAdResume
Type: Integer

Description: The number of times a user unpaused the video ad.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

videoAdSkipBacks
Type: Integer

Description: The number of times a video was skipped backwards.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

videoAdSkipForwards
Type: Integer

Description: The number of times an ad was skipped forward.

Report types: dspCampaign, dspInventory, dspProduct, dspTech, dspGeo, dspAudience

videoAdStart
Type: Integer

Description: The number of times a video ad was started.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

videoAdThirdQuartile
Type: Integer

Description: The number of times at least 75% of a video ad played. If rewind occurred, percent complete was calculated on the total percentage of unduplicated video viewed.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

videoAdUnmute
Type: Integer

Description: The number of times a user unmuted the video ad.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

videoCompleteViews
Type: Integer

Description: The number of impressions where the video was viewed to 100%.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sbSearchTerm, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, stCampaigns, stTargeting, sbAds

videoDownloadRate
Type: Integer

Description: The number of video downloads relative to the number of impressions. (Video download rate = Video downloads / Impressions)

Report types: dspCampaign, dspInventory, dspAudience

videoDownloads
Type: Integer

Description: The number of times a video was downloaded for the featured product.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

videoDownloadsClicks
Type: Integer

Description: The number of video downloads attributed to ad click-throughs.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

videoDownloadsViews
Type: Integer

Description: The number of video downloads attributed to ad impressions.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

videoFirstQuartileViews
Type: Integer

Description: The number of impressions where the video was viewed to 25%.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sbSearchTerm, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, stCampaigns, stTargeting, sbAds

videoMidpointViews
Type: Integer

Description: The number of impressions where the video was viewed to 50%.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sbSearchTerm, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, stCampaigns, stTargeting, sbAds

videoStreams
Type: Integer

Description: The number of times a video was streamed (played without downloading).

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

videoStreamsClicks
Type: Integer

Description: The number of video streams attributed to ad click-throughs.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

videoStreamsRate
Type: Integer

Description: The number of video streams relative to the number of impressions. (Video stream rate = Video streams / Impressions)

Report types: dspCampaign, dspInventory, dspAudience

videoStreamsViews
Type: Integer

Description: The number of video streams attributed to ad impressions.

Report types: dspCampaign, dspInventory, dspTech, dspGeo, dspAudience

videoThirdQuartileViews
Type: Integer

Description: The number of impressions where the video was viewed to 75%.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sbSearchTerm, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, stCampaigns, stTargeting, sbAds

videoUnmutes
Type: Integer

Description: The number of impressions where a customer unmuted the video.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sbSearchTerm, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, sbAds

viewClickThroughRate
Type: Decimal

Description: Click-through rate for views (clicks divided by views).

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sbSearchTerm, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, sbAds

viewabilityRate
Type: Decimal

Description: View-through rate (vtr). Views divided by impressions.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sbSearchTerm, sdCampaigns, sdAdGroups, sdTargeting, sdAdvertisedProduct, sbAds, dspCampaign, dspInventory

viewableImpressions
Type: Integer

Description: Number of impressions that met the Media Ratings Council (MRC) viewability standard. See viewability details at https://advertising.amazon.com/library/guides/viewability.

Report types: sbCampaigns, sbAdGroups, sbPlacement, sbTargeting, sbSearchTerm, sbAds, dspCampaign, dspInventory, dspGeo, dspTech, spPromptAdExtension

winRate
Type: Decimal

Report types: The percentage of auctions your line item won. winRate = bids won / bids. The values range from 0 to 100 where 100 represents 100%. Note this is calculated using bids won in auction directly, not impression data that may involve traffic validation.

Report types: dspBidAdjustment


