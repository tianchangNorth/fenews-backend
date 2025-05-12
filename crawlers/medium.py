import requests
import time
import json
import sys
import io

# 解决 Windows 控制台编码问题，防止 UnicodeEncodeError
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

url = "https://medium.com/_/graphql"

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
}

query = """
query WebInlineRecommendedFeedQuery($paging: PagingOptions, $forceRank: Boolean) {\n  webRecommendedFeed(paging: $paging, forceRank: $forceRank) {\n    items {\n      ...InlineFeed_homeFeedItem\n      reasonString\n      __typename\n    }\n    pagingInfo {\n      next {\n        limit\n        to\n        source\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment userUrl_user on User {\n  __typename\n  id\n  customDomainState {\n    live {\n      domain\n      __typename\n    }\n    __typename\n  }\n  hasSubdomain\n  username\n}\n\nfragment UserAvatar_user on User {\n  __typename\n  id\n  imageId\n  membership {\n    tier\n    __typename\n    id\n  }\n  name\n  username\n  ...userUrl_user\n}\n\nfragment SignInOptions_user on User {\n  id\n  name\n  __typename\n}\n\nfragment SignUpOptions_user on User {\n  id\n  name\n  __typename\n}\n\nfragment SusiContainer_user on User {\n  ...SignInOptions_user\n  ...SignUpOptions_user\n  __typename\n  id\n}\n\nfragment SusiClickable_user on User {\n  ...SusiContainer_user\n  __typename\n  id\n}\n\nfragment UserFollowButtonSignedOut_user on User {\n  id\n  ...SusiClickable_user\n  __typename\n}\n\nfragment UserFollowButton_user on User {\n  id\n  name\n  ...UserFollowButtonSignedOut_user\n  __typename\n}\n\nfragment useIsVerifiedBookAuthor_user on User {\n  verifications {\n    isBookAuthor\n    __typename\n  }\n  __typename\n  id\n}\n\nfragment UserMentionTooltip_user on User {\n  id\n  name\n  bio\n  ...UserAvatar_user\n  ...UserFollowButton_user\n  ...useIsVerifiedBookAuthor_user\n  __typename\n}\n\nfragment PostPreviewReason_user on User {\n  name\n  ...userUrl_user\n  ...UserMentionTooltip_user\n  __typename\n  id\n}\n\nfragment PostPreviewReason_tag on Tag {\n  normalizedTagSlug\n  id\n  displayTitle\n  __typename\n}\n\nfragment PostPreviewReason_postProviderExplanation on PostProviderExplanation {\n  reason\n  interactedUsers {\n    ...PostPreviewReason_user\n    __typename\n  }\n  tagObject {\n    ...PostPreviewReason_tag\n    __typename\n    id\n  }\n  __typename\n}\n\nfragment StreamPostPreview_postProviderExplanation on PostProviderExplanation {\n  ...PostPreviewReason_postProviderExplanation\n  __typename\n}\n\nfragment StreamPostPreviewImage_imageMetadata on ImageMetadata {\n  id\n  focusPercentX\n  focusPercentY\n  alt\n  __typename\n}\n\nfragment StreamPostPreviewImage_post on Post {\n  title\n  previewImage {\n    ...StreamPostPreviewImage_imageMetadata\n    __typename\n    id\n  }\n  __typename\n  id\n}\n\nfragment SusiContainer_post on Post {\n  id\n  creator {\n    id\n    __typename\n  }\n  __typename\n}\n\nfragment SusiClickable_post on Post {\n  id\n  mediumUrl\n  ...SusiContainer_post\n  __typename\n}\n\nfragment MultiVoteCount_post on Post {\n  id\n  __typename\n}\n\nfragment MultiVote_post on Post {\n  id\n  creator {\n    id\n    ...SusiClickable_user\n    __typename\n  }\n  isPublished\n  ...SusiClickable_post\n  collection {\n    id\n    slug\n    __typename\n  }\n  isLimitedState\n  ...MultiVoteCount_post\n  __typename\n}\n\nfragment PostPreviewFooterSocial_post on Post {\n  id\n  ...MultiVote_post\n  allowResponses\n  isPublished\n  isLimitedState\n  postResponses {\n    count\n    __typename\n  }\n  __typename\n}\n\nfragment AddToCatalogBase_post on Post {\n  id\n  isPublished\n  ...SusiClickable_post\n  __typename\n}\n\nfragment AddToCatalogBookmarkButton_post on Post {\n  ...AddToCatalogBase_post\n  __typename\n  id\n}\n\nfragment BookmarkButton_post on Post {\n  visibility\n  ...SusiClickable_post\n  ...AddToCatalogBookmarkButton_post\n  __typename\n  id\n}\n\nfragment ClapMutation_post on Post {\n  __typename\n  id\n  clapCount\n  ...MultiVoteCount_post\n}\n\nfragment OverflowMenuItemUndoClaps_post on Post {\n  id\n  clapCount\n  ...ClapMutation_post\n  __typename\n}\n\nfragment NegativeSignalModal_publisher on Publisher {\n  __typename\n  id\n  name\n}\n\nfragment NegativeSignalModal_post on Post {\n  id\n  creator {\n    ...NegativeSignalModal_publisher\n    viewerEdge {\n      id\n      isMuting\n      __typename\n    }\n    __typename\n    id\n  }\n  collection {\n    ...NegativeSignalModal_publisher\n    viewerEdge {\n      id\n      isMuting\n      __typename\n    }\n    __typename\n    id\n  }\n  __typename\n}\n\nfragment ExplicitSignalMenuOptions_post on Post {\n  ...NegativeSignalModal_post\n  __typename\n  id\n}\n\nfragment OverflowMenu_post on Post {\n  id\n  creator {\n    id\n    __typename\n  }\n  collection {\n    id\n    __typename\n  }\n  ...OverflowMenuItemUndoClaps_post\n  ...AddToCatalogBase_post\n  ...ExplicitSignalMenuOptions_post\n  __typename\n}\n\nfragment OverflowMenuButton_post on Post {\n  id\n  visibility\n  ...OverflowMenu_post\n  __typename\n}\n\nfragment PostPreviewFooterMenu_post on Post {\n  id\n  ...BookmarkButton_post\n  ...OverflowMenuButton_post\n  __typename\n}\n\nfragment usePostPublishedAt_post on Post {\n  firstPublishedAt\n  latestPublishedAt\n  pinnedAt\n  __typename\n  id\n}\n\nfragment Star_post on Post {\n  id\n  creator {\n    id\n    __typename\n  }\n  isLocked\n  __typename\n}\n\nfragment PostPreviewFooterMeta_post on Post {\n  isLocked\n  postResponses {\n    count\n    __typename\n  }\n  ...usePostPublishedAt_post\n  ...Star_post\n  __typename\n  id\n}\n\nfragment PostPreviewFooter_post on Post {\n  ...PostPreviewFooterSocial_post\n  ...PostPreviewFooterMenu_post\n  ...PostPreviewFooterMeta_post\n  __typename\n  id\n}\n\nfragment UserName_user on User {\n  name\n  ...useIsVerifiedBookAuthor_user\n  ...userUrl_user\n  ...UserMentionTooltip_user\n  __typename\n  id\n}\n\nfragment PostPreviewByLineAuthor_user on User {\n  ...UserMentionTooltip_user\n  ...UserAvatar_user\n  ...UserName_user\n  __typename\n  id\n}\n\nfragment collectionUrl_collection on Collection {\n  id\n  domain\n  slug\n  __typename\n}\n\nfragment CollectionAvatar_collection on Collection {\n  name\n  avatar {\n    id\n    __typename\n  }\n  ...collectionUrl_collection\n  __typename\n  id\n}\n\nfragment SignInOptions_collection on Collection {\n  id\n  name\n  __typename\n}\n\nfragment SignUpOptions_collection on Collection {\n  id\n  name\n  __typename\n}\n\nfragment SusiContainer_collection on Collection {\n  name\n  ...SignInOptions_collection\n  ...SignUpOptions_collection\n  __typename\n  id\n}\n\nfragment SusiClickable_collection on Collection {\n  ...SusiContainer_collection\n  __typename\n  id\n}\n\nfragment CollectionFollowButton_collection on Collection {\n  __typename\n  id\n  slug\n  name\n  ...SusiClickable_collection\n}\n\nfragment EntityPresentationRankedModulePublishingTracker_entity on RankedModulePublishingEntity {\n  __typename\n  ... on Collection {\n    id\n    __typename\n  }\n  ... on User {\n    id\n    __typename\n  }\n}\n\nfragment CollectionTooltip_collection on Collection {\n  id\n  name\n  slug\n  description\n  subscriberCount\n  customStyleSheet {\n    header {\n      backgroundImage {\n        id\n        __typename\n      }\n      __typename\n    }\n    __typename\n    id\n  }\n  ...CollectionAvatar_collection\n  ...CollectionFollowButton_collection\n  ...EntityPresentationRankedModulePublishingTracker_entity\n  __typename\n}\n\nfragment CollectionLinkWithPopover_collection on Collection {\n  name\n  ...collectionUrl_collection\n  ...CollectionTooltip_collection\n  __typename\n  id\n}\n\nfragment PostPreviewByLineCollection_collection on Collection {\n  ...CollectionAvatar_collection\n  ...CollectionTooltip_collection\n  ...CollectionLinkWithPopover_collection\n  __typename\n  id\n}\n\nfragment PostPreviewByLine_post on Post {\n  creator {\n    ...PostPreviewByLineAuthor_user\n    __typename\n    id\n  }\n  collection {\n    ...PostPreviewByLineCollection_collection\n    __typename\n    id\n  }\n  __typename\n  id\n}\n\nfragment PostPreviewInformation_post on Post {\n  readingTime\n  isLocked\n  ...Star_post\n  ...usePostPublishedAt_post\n  __typename\n  id\n}\n\nfragment StreamPostPreviewContent_post on Post {\n  id\n  title\n  previewImage {\n    id\n    __typename\n  }\n  extendedPreviewContent {\n    subtitle\n    __typename\n  }\n  ...StreamPostPreviewImage_post\n  ...PostPreviewFooter_post\n  ...PostPreviewByLine_post\n  ...PostPreviewInformation_post\n  __typename\n}\n\nfragment PostScrollTracker_post on Post {\n  id\n  collection {\n    id\n    __typename\n  }\n  sequence {\n    sequenceId\n    __typename\n  }\n  __typename\n}\n\nfragment usePostUrl_post on Post {\n  id\n  creator {\n    ...userUrl_user\n    __typename\n    id\n  }\n  collection {\n    id\n    domain\n    slug\n    __typename\n  }\n  isSeries\n  mediumUrl\n  sequence {\n    slug\n    __typename\n  }\n  uniqueSlug\n  __typename\n}\n\nfragment PostPreviewContainer_post on Post {\n  id\n  extendedPreviewContent {\n    isFullContent\n    __typename\n  }\n  visibility\n  pinnedAt\n  ...PostScrollTracker_post\n  ...usePostUrl_post\n  __typename\n}\n\nfragment StreamPostPreview_post on Post {\n  id\n  ...StreamPostPreviewContent_post\n  ...PostPreviewContainer_post\n  __typename\n}\n\nfragment InlineFeed_homeFeedItem on HomeFeedItem {\n  feedId\n  moduleSourceEncoding\n  reason\n  postProviderExplanation {\n    ...StreamPostPreview_postProviderExplanation\n    __typename\n  }\n  post {\n    ...StreamPostPreview_post\n    __typename\n    id\n  }\n  __typename\n}\n
"""

def get_medium_articles():
    results = []
    has_next_page = True

    variables = {
      "forceRank":True,
      "paging": {
        "source":"f25fce8c-de87-4885-9c9f-3dad0f183492",
        "limit":25,
        "to": "0",          
      }
    }

    while has_next_page:

        response = requests.post(url, headers=headers, json={"query": query, "variables": variables})
        
        if response.status_code != 200:
            print("❌ 请求失败:", response.status_code, response.text)
            break

        data = response.json()
        try:
            feed = data["data"]["webRecommendedFeed"]
        except KeyError:
            print("❌ 数据格式异常:", data)
            break

        items = feed.get("items", [])
        for item in items:
            post = item.get("post", {})
            results.append({
                "title": post.get("title"),
                "url": post.get("mediumUrl"),
                "img":f"https://miro.medium.com/v2/resize:fit:720/format:webp/{post.get("previewImage", {}).get("id")}" ,
                "brief": post.get("extendedPreviewContent", {}).get("subtitle"),
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(post.get("firstPublishedAt")/1000)),
            })
        
        paging_info = feed.get("pagingInfo")
        if paging_info and paging_info.get("hasNextPage"):
            cursor = paging_info.get("next")
            time.sleep(0.3)  # 适当延迟，避免被封
        else:
            break

    return results

if __name__ == "__main__":
    articles = get_medium_articles()
    print(json.dumps(articles, ensure_ascii=False, indent=2))
