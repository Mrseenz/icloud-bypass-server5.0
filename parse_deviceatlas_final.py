import json
import re

def parse_device_atlas_data(text_content):
    device_map = {}
    lines = text_content.splitlines()
    data_lines = []
    recording = False

    # Try to find the precise start and end markers from the prompt
    # The prompt states: "The relevant data starts from the line containing "iPhone 16e"
    # and continues down to the line containing "iPhone iPhone1,1"."
    # This implies these lines are unique enough as markers.

    start_marker_found = False
    for line_idx, line_content in enumerate(lines):
        if "iPhone 16e iPhone17,5 2025" in line_content:
            start_marker_found = True
            # The data includes this line, so start from here
            for data_line_idx in range(line_idx, len(lines)):
                current_data_line = lines[data_line_idx]
                data_lines.append(current_data_line)
                if "iPhone iPhone1,1 2007" in current_data_line: # End marker
                    recording = True # Indicates successful capture of the block
                    break
            if recording: # Block captured
                break

    if not recording: # Fallback if exact block not found (e.g. content changed slightly)
                      # This part is tricky and might need adjustment if website structure changes often
        data_lines = [] # Reset data_lines
        temp_recording = False
        for line in lines:
            if "Model Model Identifiers Year Released" in line: # A common header before the table
                temp_recording = True
                data_lines = [] # Clear previous attempts if any
                continue
            if temp_recording and line.strip() == "": # Empty line might signify end of table or section
                if data_lines: # if we have collected some data
                    break
            if temp_recording:
                 # Basic filter: lines that seem to start with a model name and have an identifier
                if re.match(r'^(iPhone|iPad|iPod)', line.strip()):
                    data_lines.append(line)


    processed_lines = []
    for line in data_lines:
        # Remove "Mobile Phone" or "Tablet" and subsequent text to simplify parsing
        line_simplified = re.sub(r'\s+(Mobile Phone|Tablet)\s+.*$', '', line)
        # Also remove "With Client-side" column if it's there and not useful
        line_simplified = re.sub(r'\s+(iPhone|iPad|iPod|Watch|Apple TV)\s*$', '', line_simplified, flags=re.IGNORECASE)
        processed_lines.append(line_simplified.strip())

    current_model_name = ""
    for line in processed_lines:
        if not line or "Model Model Identifiers Year Released" in line :
            continue

        # Attempt to identify model name and identifiers
        # A model name can be multiple words. Identifiers start with iPhoneX,Y or iPadX,Y.
        # A year (4 digits) usually follows the identifiers.

        # Try to split the line by finding the first occurrence of a model identifier pattern.
        # This is more robust than splitting by spaces.
        # (?:iPhone|iPad|ipad|iphone) ensures we find an identifier
        # \d{1,2},\d{1,2} is the common X,Y part
        # \s+\d{4} looks for a year following, to help delimit identifiers from model names

        # First, try to extract parts based on year and identifier pattern
        match = re.match(r'^(.*?)\s+((?:(?:iPhone|iPad|ipad|iphone)\d{1,2},\d{1,2}\s*)+)\s*(\d{4})?', line)

        if match:
            model_name_full = match.group(1).strip()
            identifiers_str = match.group(2).strip()
            # year = match.group(3) # Year is captured but not directly used for map keys/values
        else:
            # Fallback for lines that might not have a year or have a simpler structure
            # e.g. "iPhone iPhone1,1"
            simple_match = re.match(r'^(.*?)\s+((?:(?:iPhone|iPad|ipad|iphone)\d{1,2},\d{1,2}\s*)+)$', line)
            if simple_match:
                model_name_full = simple_match.group(1).strip()
                identifiers_str = simple_match.group(2).strip()
            else:
                # If line doesn't match expected structure, it might be a continuation or noise
                # Or if the model name is the same as the previous line (e.g. for multiple identifier lines)
                # This part is tricky; the provided text doesn't seem to have multi-line model names
                # but if it did, we'd need to carry `current_model_name`
                continue


        if not model_name_full or not identifiers_str:
            continue

        # Handle model name slashes as per prompt
        if '/' in model_name_full:
            model_name_full = model_name_full.split('/')[0].strip()

        # Filter out any parts of model_name_full that are actually years if misparsed
        model_name_full = re.sub(r'\s+\d{4}$', '', model_name_full).strip()


        # Extract individual identifiers from the string of identifiers
        raw_identifiers = re.findall(r'(?:iPhone|iPad|ipad|iphone)\d{1,2},\d{1,2}', identifiers_str)

        for identifier in raw_identifiers:
            identifier = identifier.strip()
            # Normalize capitalization
            if identifier.lower().startswith('iphone'):
                normalized_identifier = 'iPhone' + identifier[len('iphone'):]
            elif identifier.lower().startswith('ipad'):
                normalized_identifier = 'iPad' + identifier[len('ipad'):]
            else:
                continue

            device_map[normalized_identifier] = model_name_full

    return device_map

# Text content will be replaced by the actual fetched content by the calling agent
actual_fetched_text = """
    websights linkedin

   IFRAME: [1]https://grok.ie/js-agg/empty.html

   [2]DeviceAtlas DeviceAtlas
     * [3]Login
     * [4]Get started

     * [5]Products
          + Web
            [6]DeviceAtlas for Web
            Build enterprise grade device awareness
            into your products and services
          + Apps
            [7]DeviceAtlas for Apps
            Device intelligence, targeting and reporting
            in the native apps environment
          + Operators
            [8]Device Map
            Fine grained device intelligence
            indexed by TAC/IMEI
          + DeviceAssure
            [9]DeviceAssure
            Verify the authenticity of devices
            accessing your content and services
          + DeviceAtlas Discover
            [10]DeviceAtlas Discover
            Rich insights about your web traffic that
            analytics platforms don’t tell you about
       DEVICE INTELLIGENCE

Learn more with our
intro video
       Deliver an amazing customer
       experience across devices.
       [11]TECHNOLOGY OVERVIEW
       Get an overview of our technology.
     * [12]Use Cases
          + Ad-Tech
            [13]AdTech
            Enable granular device targeting of your campaigns.
            Maximize revenue from impressions and reduce discrepancies
          + Optimization
            [14]Web Optimization
            Ensure content is delivered in a form that’s
            optimized for the end user’s device
          + Analytics
            [15]Analytics
            Understand customer engagement at
            device level
          + Internet of Things
            [16]Internet of Things
            Measure IoT activity on your network
          + OTT Streaming
            [17]Online Streaming Services
            Identity OTT traffic from STBs, Smart
            TVs, and Games Consoles
          + eCommerce
            [18]eCommerce
            Identify factors affecting cart abandonment rates, and ensure
            optimal user experiences for mobile devices.
          + Gaming
            [19]Gaming
            Enhance knowledge of gaming devices for better analytics and
            reporting, real-time QoS/QoE monitoring, and more relevant
            targeting opportunities.
          + Reverse Logistics
            [20]Reverse Logistics
            -
          + Device Insurance
            [21]Device Insurance
            -
       CASE STUDIES

Learn how market
leaders are using us
to outperform their
competition
       Adoppler and our partners have experienced significant improvements
       since implementing DeviceAtlas.
       Anton Tkachuk
       Product Manager, Adoppler
       [22]View all case studies
     * [23]Pricing
     * [24]Developers
          + [25]Technology Overview
            Get an overview of our technology
          + [26]Getting Started
            Step by step guide to get up and running fast
          + [27]APIs
            Downloads and information on all APIs
          + [28]About the data
            Device data and available properties
          + [29]Docs & Support
            FAQ's documentation and support
          + [30]Knowledge Base
            Explore our expansive library of free
            whitepapers, eBooks and how-to guide
     * [31]Data & Insights
          + [32]Blog
            Stay informed with our articles on device
            research, data and insights
          + [33]Case Studies
            See why market leaders choose DeviceAtlas
          + [34]Device Browser
            Device information and properties
          + [35]Data Explorer
            Explore and analyse DeviceAtlas data
          + [36]Properties
            Check out our available device properties
          + [37]HTTP Headers Parser
            Check DeviceAtlas results for HTTP Headers

     * [38]Login
     * [39]Get started

   [40]Log in[41]Sign up
   Username* ____________________
   Password* ____________________
   [X] Remember me
   [42]Forgot Password?
   Log in

   Sign up below to view device data and get your trial account.
   5+2=? ____________________________________________________________
   Username* ____________________
   E-mail* ____________________
   Password* ____________________
   Confirm Password* ____________________

   [ ] We communicate via email to process your request in line with our
   [43]privacy policy. Please check the box to give us your permission to
   do this.
   Sign up
   [44]Cancel

     * [45]Products
     *
          + [46]DeviceAtlas for Web
          + [47]DeviceAtlas for Apps
          + [48]Device Map
          + [49]DeviceAssure
          + [50]DeviceAtlas Discover
          + [51]Technology Overview
     * [52]Use Cases
     *
          + [53]AdTech
          + [54]Web Optimization
          + [55]Analytics
          + [56]Internet of Things
          + [57]Online Streaming Services
          + [58]eCommerce
          + [59]Gaming
          + [60]Reverse Logistics
          + [61]Device Insurance
          + [62]Case Studies
     * [63]Pricing
     * [64]Developers
     *
          + [65]Technology Overview
          + [66]Getting Started
          + [67]APIs
          + [68]About the Data
          + [69]Docs & Support
          + [70]Knowledge Base
     * [71]Data & Insights
     *
          + [72]Blog
          + [73]Case Studies
          + [74]Device Browser
          + [75]Data Explorer
          + [76]Properties
          + [77]HTTP Headers Parser
     * [78]Login
     * [79]Get started
     *

   Resources →

Getting Started

     * [80]Enterprise
          + [81]DeviceAtlas for Web
          + [82]DeviceAtlas for Apps
     * [83]Cloud
     * [84]DeviceAssure
          + [85]DeviceAssure for Web
          + [86]DeviceAssure for Apps
     * [87]Discover

APIs

     * [88]Enterprise APIs
          + [89]Download API
          + [90]Documentation
          + [91]API examples
          + [92]Performance
     * [93]Cloud Service
          + [94]Download API
          + [95]Documentation
          + [96]Cloud Service End-Points
          + [97]Google Sheets Integration
     * [98]DeviceAssure APIs
          + [99]Download API
          + [100]Documentation
     * [101]Client-side Component
          + [102]iOS H/W Identification
          + [103]Usage
          + [104]Download
     * [105]REST API
     * [106]User-Agent Client Hints
          + [107]Developer considerations
          + [108]Web server configuration
          + [109]OpenRTB and UA-CH
          + [110]Capturing in JavaScript
          + [111]Header precedence logic

Data

     * [112]Data Downloads
          + [113]Carrier Data
          + [114]Device Data (JSON)
          + [115]Device Map (TAC)
     * [116]Data File Configuration
     * [117]Contributing
     * [118]About Our Data
     * [119]Dynamic Data
     * [120]Becoming a Data Partner

Properties

     * [121]Available Properties
     * [122]Client-side Properties

FAQ

     * [123]Support
     * [124]General
     * [125]Licensing

More

     * [126]Side-loaded Browsers
     * [127]Whitepapers
     * [128]Case Studies

Resources

iOS Hardware Identification

   Resources

   The DeviceAtlas Client-side Component augments the server side
   properties and allows for precise identification of Apple devices.

   In order to facilitate iOS hardware identification, the following
   [129]Client-side properties should be enabled:
screenWidthHeight, audioRef, devicePixelRatio, rendererRef, js.webGlRenderer, js
.deviceMotion, deviceAspectRatio, html.video.ap4x, html.video.av1

   You can enable the properties on the Client-side Component
   [130]download page.

   The following variants of iPhone and iPad models are identified:

   Please note that zoom mode can affect the identification of these
   devices.
   Model Model Identifiers Year Released Primary Hardware Type Without
   Client-side With Client-side
   iPhone 16e iPhone17,5 2025 Mobile Phone iPhone iPhone 16e
   iPhone 16 iPhone17,3 2024 Mobile Phone iPhone iPhone 15 Pro/iPhone 16
   iPhone 16 Plus iPhone17,4 2024 Mobile Phone iPhone iPhone 15 Pro
   Max/iPhone 16 Plus
   iPhone 16 Pro iPhone17,1 2024 Mobile Phone iPhone iPhone 16 Pro
   iPhone 16 Pro Max iPhone17,2 2024 Mobile Phone iPhone iPhone 16 Pro Max
   iPad Air (11 6th Gen) iPad14,8
   iPad14,9 2024 Tablet iPad iPad Air 4/iPad Air 5/iPad Air (11 6th Gen)
   iPad Air (13 6th Gen) iPad14,10
   iPad14,11 2024 Tablet iPad iPad Pro (12.9 5th Gen)/iPad Pro (12.9 6th
   Gen)/iPad Air (13 6th Gen)
   iPad Pro (11 5th Gen) iPad16,3
   iPad16,4 2024 Tablet iPad iPad Pro (11 5th Gen)
   iPad Pro (13 7th Gen) iPad16,5
   iPad16,6 2024 Tablet iPad iPad Pro (13 7th Gen)
   iPhone 15 iPhone15,4 2023 Mobile Phone iPhone iPhone 14 Pro/iPhone 15
   iPhone 15 Plus iPhone15,5 2023 Mobile Phone iPhone iPhone 14 Pro
   Max/iPhone 15 Plus
   iPhone 15 Pro iPhone16,1 2023 Mobile Phone iPhone iPhone 15 Pro/iPhone
   16
   iPhone 15 Pro Max iPhone16,2 2023 Mobile Phone iPhone iPhone 15 Pro
   Max/iPhone 16 Plus
   iPad (10th Gen) iPad13,18
   iPad13,19 2022 Tablet iPad iPad (10th Gen)
   iPad Air 5 iPad13,16
   iPad13,17 2022 Tablet iPad iPad Air 4/iPad Air 5/iPad Air (11 6th Gen)
   iPad Pro (11 4th Gen) iPad14,3
   iPad14,4 2022 Tablet iPad iPad Pro (11 3rd Gen)/iPad Pro (11 4th Gen)
   iPad Pro (12.9 6th Gen) iPad14,5
   iPad14,6 2022 Tablet iPad iPad Pro (12.9 5th Gen)/iPad Pro (12.9 6th
   Gen)/iPad Air (13 6th Gen)
   iPhone 14 iPhone14,7 2022 Mobile Phone iPhone iPhone 13/iPhone 13
   Pro/iPhone 14
   iPhone 14 Plus iPhone14,8 2022 Mobile Phone iPhone iPhone 13 Pro
   Max/iPhone 14 Plus
   iPhone 14 Pro iPhone15,2 2022 Mobile Phone iPhone iPhone 14 Pro/iPhone
   15
   iPhone 14 Pro Max iPhone15,3 2022 Mobile Phone iPhone iPhone 14 Pro
   Max/iPhone 15 Plus
   iPhone SE (3rd generation) iPhone14,6 2022 Mobile Phone iPhone iPhone
   SE (3rd generation)
   iPad (9th Gen) iPad12,1
   iPad12,2
   ipad12,1 2021 Tablet iPad iPad (9th Gen)
   iPad mini 6 iPad14,1
   iPad14,2 2021 Tablet iPad iPad mini 6
   iPad Pro (11 3rd Gen) iPad13,5
   iPad13,6
   iPad13,7
   iPad13,4 2021 Tablet iPad iPad Pro (11 3rd Gen)/iPad Pro (11 4th Gen)
   iPad Pro (12.9 5th Gen) iPad13,10
   iPad13,11
   iPad13,9
   iPad13,8 2021 Tablet iPad iPad Pro (12.9 5th Gen)/iPad Pro (12.9 6th
   Gen)/iPad Air (13 6th Gen)
   iPhone 13 iPhone14,5 2021 Mobile Phone iPhone iPhone 13/iPhone 13
   Pro/iPhone 14
   iPhone 13 mini iPhone14,4 2021 Mobile Phone iPhone iPhone 13
   mini/iPhone 13 Pro Max/iPhone 14 Plus/iPhone 14 Pro Max/iPhone 15 Plus
   iPhone 13 Pro iPhone14,2 2021 Mobile Phone iPhone iPhone 13/iPhone 13
   Pro/iPhone 14
   iPhone 13 Pro Max iPhone14,3 2021 Mobile Phone iPhone iPhone 13 Pro
   Max/iPhone 14 Plus
   iPad (8th Gen) iPad11,6
   iPad11,7 2020 Tablet iPad iPad (8th Gen)
   iPad Air 4 iPad13,1
   iPad13,2 2020 Tablet iPad iPad Air 4/iPad Air 5/iPad Air (11 6th Gen)
   iPad Pro (11 2nd Gen) iPad8,9
   iPad8,10 2020 Tablet iPad iPad Pro (11)/iPad Pro (11 2nd Gen)
   iPad Pro (12.9 4th Gen) iPad8,11
   iPad8,12 2020 Tablet iPad iPad Pro (12.9 3rd Gen)/iPad Pro (12.9 4th
   Gen)
   iPhone 12 iPhone13,2 2020 Mobile Phone iPhone iPhone 12/iPhone 12 Pro
   iPhone 12 Mini iPhone13,1 2020 Mobile Phone iPhone iPhone 12
   Mini/iPhone 12 Pro Max
   iPhone 12 Pro iPhone13,3 2020 Mobile Phone iPhone iPhone 12/iPhone 12
   Pro
   iPhone 12 Pro Max iPhone13,4 2020 Mobile Phone iPhone iPhone 12 Pro Max
   iPhone SE (2nd generation) iPhone12,8 2020 Mobile Phone iPhone iPhone
   SE (2nd generation)
   iPad (7th Gen) iPad7,11
   iPad7,12 2019 Tablet iPad iPad (7th Gen)
   iPad Air 3 iPad11,3
   iPad11,4 2019 Tablet iPad iPad Air 3
   iPad mini 5 iPad11,1
   iPad11,2 2019 Tablet iPad iPad mini 5
   iPhone 11 iPhone12,1 2019 Mobile Phone iPhone iPhone 11
   iPhone 11 Pro iPhone12,3 2019 Mobile Phone iPhone iPhone 11 Pro/iPhone
   11 Pro Max
   iPhone 11 Pro Max iPhone12,5 2019 Mobile Phone iPhone iPhone 11 Pro Max
   iPad (6th Gen) iPad7,5
   iPad7,6
   ipad7,5 2018 Tablet iPad iPad (5th Gen)/iPad (6th Gen)
   iPad Pro (11) iPad8,1
   iPad8,2
   iPad8,3
   iPad8,4 2018 Tablet iPad iPad Pro (11)/iPad Pro (11 2nd Gen)
   iPad Pro (12.9 3rd Gen) iPad8,5
   iPad8,6
   iPad8,7
   iPad8,8 2018 Tablet iPad iPad Pro (12.9 3rd Gen)/iPad Pro (12.9 4th
   Gen)
   iPhone XR iPhone11,8
   iphone11,8 2018 Mobile Phone iPhone iPhone XR
   iPhone XS iPhone11,2
   iphone11,2 2018 Mobile Phone iPhone iPhone XS/iPhone XS Max
   iPhone XS Max iPhone11,4
   iPhone11,6
   iphone11,6 2018 Mobile Phone iPhone iPhone XS Max
   iPad (5th Gen) iPad6,11
   iPad6,12
   ipad6,12 2017 Tablet iPad iPad (5th Gen)/iPad (6th Gen)
   iPad Pro (10.5) iPad7,3
   iPad7,4 2017 Tablet iPad iPad Pro (10.5)
   iPad Pro (12.9 2nd Gen) iPad7,1
   iPad7,2 2017 Tablet iPad iPad Pro (12.9 2nd Gen)
   iPhone 8 iPhone10,1
   iPhone10,4
   iphone10,1
   iphone10,4 2017 Mobile Phone iPhone iPhone 8
   iPhone 8 Plus iPhone10,2
   iPhone10,5
   iphone10,5
   iphone10,2 2017 Mobile Phone iPhone iPhone 8 Plus
   iPhone X iPhone10,3
   iPhone10,6
   iphone10,3
   iphone10,6 2017 Mobile Phone iPhone iPhone X
   iPad Pro (9.7) iPad6,3
   iPad6,4 2016 Tablet iPad iPad Pro (9.7)
   iPhone 7 iPhone9,1
   iPhone9,3
   iphone9,1
   iphone9,3 2016 Mobile Phone iPhone iPhone 7
   iPhone 7 Plus iPhone9,2
   iPhone9,4
   iphone9,4
   iphone9,2 2016 Mobile Phone iPhone iPhone 7 Plus
   iPhone SE iPhone8,4
   iphone8,4 2016 Mobile Phone iPhone iPhone SE
   iPad mini 4 iPad5,1
   iPad5,2
   ipad5,2 2015 Tablet iPad iPad Air 2/iPad mini 4
   iPad Pro iPad6,7
   iPad6,8 2015 Tablet iPad iPad Pro
   iPhone 6S iPhone8,1
   iphone8,1 2015 Mobile Phone iPhone iPhone 6S
   iPhone 6S Plus iPhone8,2
   iphone8,2 2015 Mobile Phone iPhone iPhone 6S Plus
   iPad Air 2 iPad5,3
   iPad5,4
   ipad5,3 2014 Tablet iPad iPad Air 2/iPad mini 4
   iPad mini 3 iPad4,7
   iPad4,8
   iPad4,9 2014 Tablet iPad iPad Air/iPad mini 2/iPad mini 3
   iPhone 6 iPhone7,2
   iphone7,2 2014 Mobile Phone iPhone iPhone 6
   iPhone 6 Plus iPhone7,1 2014 Mobile Phone iPhone iPhone 6 Plus
   iPad Air iPad4,1
   iPad4,2
   iPad4,3 2013 Tablet iPad iPad Air/iPad mini 2/iPad mini 3
   iPad mini Retina iPad4,4
   iPad4,5
   iPad4,6 2013 Tablet iPad iPad Air/iPad mini 2/iPad mini 3
   iPhone 5C iPhone5,4
   iPhone5,3 2013 Mobile Phone iPhone iPhone 5/iPhone 5C
   iPhone 5S iPhone6,2
   iPhone6,1 2013 Mobile Phone iPhone iPhone 5S
   iPad Retina (3rd Gen) iPad3,3
   iPad3,1
   iPad3,2 2012 Tablet iPad iPad Retina (3rd Gen)
   iPad mini iPad2,5
   iPad2,6
   iPad2,7 2012 Tablet iPad iPad 2/iPad mini
   iPad Retina (4th Gen) iPad3,4
   iPad3,5
   iPad3,6 2012 Tablet iPad iPad Retina (4th Gen)
   iPhone 5 iPhone5,1
   iPhone5,2 2012 Mobile Phone iPhone iPhone 5/iPhone 5C
   iPad 2 iPad2,2
   iPad2,1
   iPad2,3
   iPad2,4 2011 Tablet iPad iPad 2/iPad mini
   iPhone 4S iPhone4,1 2011 Mobile Phone iPhone iPhone 4S
   iPad iPad1,1 2010 Tablet iPad iPad
   iPhone 4 iPhone3,3
   iPhone3,1
   iPhone3,2 2010 Mobile Phone iPhone iPhone 4
   iPhone 3GS iPhone2,1 2009 Mobile Phone iPhone iPhone/iPhone 3G/iPhone
   3GS
   iPhone 3G iPhone1,2 2008 Mobile Phone iPhone iPhone/iPhone 3G/iPhone
   3GS
   iPhone iPhone1,1 2007 Mobile Phone iPhone iPhone/iPhone 3G/iPhone 3GS

   DeviceAtlas identifies and verifies connected devices in real-time for
   rich, actionable intelligence across every customer touchpoint

Our Products

   [131]

DeviceAtlas for Web

   The full picture on web traffic with detailed metadata on all visiting
   devices
   [132]

DeviceAtlas for Apps

   Device intelligence, targeting and reporting in the native apps
   environment
   [133]

DeviceAssure

   Real-time identification of fraudulent and misrepresented traffic
   [134]

Device Map

   TAC-based device insights for the mobile ecosystem, in partnership with
   the GSMA

Industries

   [135]AdTech [136]Optimization [137]Analytics [138]Internet of Things
   [139]OTT / Streaming [140]eCommerce [141]Gaming [142]Reverse Logistics
   [143]Device Insurance

Quick links

   [144]Pricing [145]About us [146]Events [147]Blog [148]Device
   Intelligence [149]Device Detection [150]Technology Partners [151]Case
   Studies [152]Data & Insights [153]Developers [154]Contact us

   Copyright © DeviceAtlas Limited 2025. All Rights Reserved. [155]Terms &
   Conditions | [156]Privacy Policy

   This is a website of DeviceAtlas Limited, a private company limited by
   shares, incorporated and registered in the Republic of Ireland with
   registered number 398040 and registered office at 6th Floor, 2 Grand
   Canal Square, Dublin 2, Ireland
   Industry Affiliations

References

   Visible links:
   1. https://grok.ie/js-agg/empty.html
   2. https://deviceatlas.com/
   3. https://deviceatlas.com/user/login
   4. https://deviceatlas.com/get-started
   5. https://deviceatlas.com/products/overview
   6. https://deviceatlas.com/products/web
   7. https://deviceatlas.com/products/apps
   8. https://deviceatlas.com/products/mobile-operators
   9. https://deviceatlas.com/products/deviceassure
  10. https://deviceatlas.com/products/deviceatlas-discover
  11. https://deviceatlas.com/products/overview
  12. https://deviceatlas.com/case-studies
  13. https://deviceatlas.com/solutions/ad-tech
  14. https://deviceatlas.com/solutions/optimization
  15. https://deviceatlas.com/solutions/analytics
  16. https://deviceatlas.com/solutions/iot
  17. https://deviceatlas.com/solutions/streaming
  18. https://deviceatlas.com/solutions/ecommerce
  19. https://deviceatlas.com/solutions/gaming
  20. https://deviceatlas.com/solutions/reverse-logistics
  21. https://deviceatlas.com/solutions/device-insurance
  22. https://deviceatlas.com/case-studies
  23. https://deviceatlas.com/pricing
  24. https://deviceatlas.com/resources
  25. https://deviceatlas.com/products/overview
  26. https://deviceatlas.com/resources
  27. https://deviceatlas.com/resources/enterprise-apis
  28. https://deviceatlas.com/resources/getting-the-data
  29. https://deviceatlas.com/resources/support
  30. https://deviceatlas.com/knowledge-base
  31. https://deviceatlas.com/device-data/devices
  32. https://deviceatlas.com/blog
  33. https://deviceatlas.com/case-studies
  34. https://deviceatlas.com/device-data/devices
  35. https://deviceatlas.com/device-data/explorer
  36. https://deviceatlas.com/device-data/properties
  37. https://deviceatlas.com/device-data/user-agent-tester
  38. https://deviceatlas.com/user/login
  39. https://deviceatlas.com/get-started
  40. https://deviceatlas.com/resources/clientside/ios-hardware-identification
  41. https://deviceatlas.com/resources/clientside/ios-hardware-identification
  42. https://deviceatlas.com/user/password
  43. https://deviceatlas.com/privacy-policy
  44. https://deviceatlas.com/resources/clientside/ios-hardware-identification
  45. https://deviceatlas.com/products/overview
  46. https://deviceatlas.com/products/web
  47. https://deviceatlas.com/products/apps
  48. https://deviceatlas.com/products/mobile-operators
  49. https://deviceatlas.com/products/deviceassure
  50. https://deviceatlas.com/products/deviceatlas-discover
  51. https://deviceatlas.com/products/overview
  52. https://deviceatlas.com/case-studies
  53. https://deviceatlas.com/solutions/ad-tech
  54. https://deviceatlas.com/solutions/optimization
  55. https://deviceatlas.com/solutions/analytics
  56. https://deviceatlas.com/solutions/iot
  57. https://deviceatlas.com/solutions/streaming
  58. https://deviceatlas.com/solutions/ecommerce
  59. https://deviceatlas.com/solutions/gaming
  60. https://deviceatlas.com/solutions/reverse-logistics
  61. https://deviceatlas.com/solutions/device-insurance
  62. https://deviceatlas.com/case-studies
  63. https://deviceatlas.com/pricing
  64. https://deviceatlas.com/resources
  65. https://deviceatlas.com/products/overview
  66. https://deviceatlas.com/resources
  67. https://deviceatlas.com/resources/enterprise-apis
  68. https://deviceatlas.com/resources/getting-the-data
  69. https://deviceatlas.com/resources/support
  70. https://deviceatlas.com/knowledge-base
  71. https://deviceatlas.com/device-data/devices
  72. https://deviceatlas.com/blog
  73. https://deviceatlas.com/case-studies
  74. https://deviceatlas.com/device-data/devices
  75. https://deviceatlas.com/device-data/explorer
  76. https://deviceatlas.com/device-data/properties
  77. https://deviceatlas.com/device-data/user-agent-tester
  78. https://deviceatlas.com/user/login
  79. https://deviceatlas.com/resources
  80. https://deviceatlas.com/resources/getting-started-enterprise
  81. https://deviceatlas.com/resources/getting-started-enterprise-for-web
  82. https://deviceatlas.com/resources/getting-started-enterprise-for-apps
  83. https://deviceatlas.com/resources/getting-started-cloud
  84. https://deviceatlas.com/resources/getting-started-deviceassure
  85. https://deviceatlas.com/resources/getting-started-deviceassure-for-web
  86. https://deviceatlas.com/resources/getting-started-deviceassure-for-apps
  87. https://deviceatlas.com/resources/getting-deviceatlas-discover
  88. https://deviceatlas.com/resources/enterprise-apis
  89. https://deviceatlas.com/resources/download-enterprise-api
  90. https://deviceatlas.com/resources/enterprise-api-documentation
  91. https://deviceatlas.com/resources/example-code
  92. https://deviceatlas.com/resources/enterprise-api-performance
  93. https://deviceatlas.com/resources/cloud-apis
  94. https://deviceatlas.com/resources/download-cloud-api
  95. https://deviceatlas.com/resources/cloud-api-documentation
  96. https://deviceatlas.com/resources/cloud-service-end-points
  97. https://deviceatlas.com/resources/google-sheets-integration
  98. https://deviceatlas.com/resources/deviceassure-apis
  99. https://deviceatlas.com/resources/download-deviceassure-api
 100. https://deviceatlas.com/resources/deviceassure-api-documentation
 101. https://deviceatlas.com/resources/clientside
 102. https://deviceatlas.com/resources/clientside/ios-hardware-identification
 103. https://deviceatlas.com/resources/clientside/usage
 104. https://deviceatlas.com/resources/clientside/download
 105. https://deviceatlas.com/resources/rest-api
 106. https://deviceatlas.com/resources/user-agent-client-hints
 107. https://deviceatlas.com/resources/user-agent-client-hints-developer-considerations
 108. https://deviceatlas.com/resources/configuring-nginx-and-apache-support-user-agent-client-hints
 109. https://deviceatlas.com/resources/user-agent-client-hints-and-openrtb
 110. https://deviceatlas.com/resources/capturing-user-agent-client-hint-data-browser-javascript
 111. https://deviceatlas.com/resources/deviceatlas-and-ua-ch-header-precedence
 112. https://deviceatlas.com/resources/getting-the-data
 113. https://deviceatlas.com/resources/getting-the-data/carrier-data
 114. https://deviceatlas.com/resources/getting-the-data/device-data
 115. https://deviceatlas.com/resources/getting-the-data/device-map
 116. https://deviceatlas.com/resources/customizing-data
 117. https://deviceatlas.com/resources/contributing-data
 118. https://deviceatlas.com/resources/about-our-data
 119. https://deviceatlas.com/resources/dynamic-data
 120. https://deviceatlas.com/resources/becoming-data-partner
 121. https://deviceatlas.com/resources/available-properties
 122. https://deviceatlas.com/resources/client-side-properties
 123. https://deviceatlas.com/resources/support
 124. https://deviceatlas.com/resources/general
 125. https://deviceatlas.com/resources/licencing
 126. https://deviceatlas.com/resources/side-loaded-browser-handling
 127. https://deviceatlas.com/whitepapers
 128. https://deviceatlas.com/case-studies
 129. https://deviceatlas.com/resources/client-side-properties
 130. https://deviceatlas.com/resources/clientside/download
 131. https://deviceatlas.com/products/web
 132. https://deviceatlas.com/products/apps
 133. https://deviceatlas.com/products/deviceassure
 134. https://deviceatlas.com/products/mobile-operators
 135. https://deviceatlas.com/solutions/ad-tech
 136. https://deviceatlas.com/solutions/optimization
 137. https://deviceatlas.com/solutions/analytics
 138. https://deviceatlas.com/solutions/iot
 139. https://deviceatlas.com/solutions/streaming
 140. https://deviceatlas.com/solutions/ecommerce
 141. https://deviceatlas.com/solutions/gaming
 142. https://deviceatlas.com/solutions/reverse-logistics
 143. https://deviceatlas.com/solutions/device-insurance
 144. https://deviceatlas.com/pricing
 145. https://deviceatlas.com/about-us
 146. https://deviceatlas.com/events
 147. https://deviceatlas.com/blog
 148. https://deviceatlas.com/device-intelligence
 149. https://deviceatlas.com/device-detection
 150. https://deviceatlas.com/technology-partners
 151. https://deviceatlas.com/case-studies
 152. https://deviceatlas.com/device-data/devices
 153. https://deviceatlas.com/resources
 154. https://deviceatlas.com/contact
 155. https://deviceatlas.com/terms-conditions
 156. https://deviceatlas.com/privacy-policy

   Hidden links:
 158. https://deviceatlas.com/products/web
 159. https://deviceatlas.com/products/apps
 160. https://deviceatlas.com/products/mobile-operators
 161. https://deviceatlas.com/products/deviceassure
 162. https://deviceatlas.com/products/deviceatlas-discover
 163. https://deviceatlas.com/solutions/ad-tech
 164. https://deviceatlas.com/solutions/optimization
 165. https://deviceatlas.com/solutions/analytics
 166. https://deviceatlas.com/solutions/iot
 167. https://deviceatlas.com/solutions/streaming
 168. https://deviceatlas.com/solutions/ecommerce
 169. https://deviceatlas.com/solutions/gaming
 170. https://deviceatlas.com/solutions/reverse-logistics
 171. https://deviceatlas.com/solutions/device-insurance
 172. https://deviceatlas.com/products/overview
 173. https://deviceatlas.com/resources
 174. https://deviceatlas.com/resources/enterprise-apis
 175. https://deviceatlas.com/resources/getting-the-data
 176. https://deviceatlas.com/resources/support
 177. https://deviceatlas.com/knowledge-base
 178. https://deviceatlas.com/blog
 179. https://deviceatlas.com/case-studies
 180. https://deviceatlas.com/device-data/devices
 181. https://deviceatlas.com/device-data/explorer
 182. https://deviceatlas.com/device-data/properties
 183. https://deviceatlas.com/device-data/user-agent-tester
 184. https://deviceatlas.com/search
 185. https://deviceatlas.com/search
 186. https://www.linkedin.com/company/deviceatlas/
 187. https://twitter.com/Device_Atlas
 188. https://www.youtube.com/@DeviceAtlas
 Warning: User-Agent string does not contain "Lynx" or "L_y_n_x"!
"""

result_map = parse_device_atlas_data(actual_fetched_text)
print(json.dumps(result_map)) # Ensure only JSON is printed
