<?php
/*
 * deviceservices/config.php
 *
 * This configuration file is used by `deviceActivation.php` to externalize various
 * parameters required for iDevice activation, certificate signing, and token generation.
 *
 * Configuration Keys:
 *
 * - certs_path: (string)
 *   Base path for certificate-related files (e.g., CA certificate, keys, extensions).
 *   Ensure this path is correct relative to the `deviceservices` directory or use an absolute path.
 *
 * - signing_days: (int)
 *   The validity period in days for locally signed device certificates.
 *
 * - ca_private_key_passphrase: (string)
 *   The passphrase used to encrypt the CA private key (`ca_private_key_file`).
 *
 * - device_cert_serial_number: (string)
 *   The serial number to be used for the device certificate signed by the local CA.
 *   This should be a hexadecimal string (e.g., '0x012345ABCDEF').
 *
 * - ca_cert_file: (string) Relative to `certs_path`.
 *   The filename of the CA certificate (e.g., 'iPhoneDeviceCA.crt').
 *   If you regenerate your CA certificate (e.g., to use SHA-256), ensure this points to the correct file.
 *
 * - ca_private_key_file: (string) Relative to `certs_path`.
 *   The filename of the CA private key (e.g., 'iPhoneDeviceCA_private.key').
 *
 * - openssl_extensions_file: (string) Relative to `certs_path`.
 *   The OpenSSL extensions configuration file used during certificate signing (e.g., 'extensions_device.cnf').
 *
 * - wildcard_ticket_file: (string) Relative to `certs_path`.
 *   Path to the wildcard ticket file, which is included in the account token.
 *   (e.g., 'ext/wildcardticket.txt')
 *
 * - account_token_signing_key_file: (string) Relative to `certs_path`.
 *   Private key used for signing the account token (e.g., 'signature_private.key').
 *
 * - account_token_urls: (array)
 *   An array of URLs that are embedded into the account token sent to the device.
 *   - 'activity': URL for device activity/reporting.
 *   - 'certify_me': URL for device certificate validation/authentication.
 *   - 'phone_home': URL for device "phone home" or check-in operations.
 *
 * - fairplay_account_token_certificate_base64: (string)
 *   Base64 encoded FairPlay Account Token Certificate. This is a long string.
 *   This data is typically specific to device models and iOS versions.
 *   For a custom activation server, this might need to be sourced from actual device
 *   interactions or updated periodically if aiming for compatibility with newer devices/iOS.
 *
 * - fairplay_key_data_base64: (string)
 *   Base64 encoded FairPlay Key Data. This is also a long string.
 *   Similar to the certificate, this data is device/iOS specific and may require
 *   updating for broader compatibility.
 *
 * How to Update Values:
 * - Paths: Ensure all paths, especially `certs_path` and files relative to it, are correct.
 *   You can use paths relative to the `deviceservices` directory or absolute paths if preferred.
 * - Certificates/Keys: If you regenerate your CA (e.g., to use SHA-256 for its signature) or
 *   other keys, make sure the corresponding file paths and passphrases in this config are updated.
 * - FairPlay Data: The base64 strings for FairPlay are often the most challenging to maintain.
 *   If activations fail for newer devices, these values might be a factor.
 */

return [
    'certs_path' => 'certs/',
    'signing_days' => 1096,
    'ca_private_key_passphrase' => 'icloud',
    'device_cert_serial_number' => '0x02A590E676E2CEED3A99',

    'ca_cert_file' => 'iPhoneDeviceCA.crt', // Relative to certs_path
    'ca_private_key_file' => 'iPhoneDeviceCA_private.key', // Relative to certs_path
    'openssl_extensions_file' => 'extensions_device.cnf', // Relative to certs_path
    'wildcard_ticket_file' => 'ext/wildcardticket.txt', // Relative to certs_path
    'account_token_signing_key_file' => 'signature_private.key', // Relative to certs_path

    'account_token_urls' => [
        'activity' => 'https://albert.apple.com/deviceservices/activity',
        'certify_me' => 'https://albert.apple.com/deviceservices/certifyMe',
        'phone_home' => 'https://albert.apple.com/deviceservices/phoneHome',
    ],

    'fairplay_account_token_certificate_base64' => 'LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURaekNDQWsrZ0F3SUJBZ0lCQWpBTkJna3Foa2lHOXcwQkFRVUZBREI1TVFzd0NRWURWUVFHRXdKVlV6RVQKTUJFR0ExVUVDaE1LUVhCd2JHVWdTVzVqTGpFbU1DUUdBMVVFQ3hNZFFYQndiR1VnUTJWeWRHbG1hV05oZEdsdgpiaUJCZFhSb2IzSnBkSGt4TFRBckJnTlZCQU1USkVGd2NHeGxJR2xRYUc5dVpTQkRaWEowYVdacFkyRjBhVzl1CklFRjFkR2h2Y21sMGVUQWVGdzB3TnpBME1UWXlNalUxTURKYUZ3MHhOREEwTVRZeU1qVTFNREphTUZzeEN6QUoKQmdOVkJBWVRBbFZUTVJNd0VRWURWUVFLRXdwQmNIQnNaU0JKYm1NdU1SVXdFd1lEVlFRTEV3eEJjSEJzWlNCcApVR2h2Ym1VeElEQWVCZ05WQkFNVEYwRndjR3hsSUdsUWFHOXVaU0JCWTNScGRtRjBhVzl1TUlHZk1BMEdDU3FHClNJYjNEUUVCQVFVQUE0R05BRENCaVFLQmdRREZBWHpSSW1Bcm1vaUhmYlMyb1BjcUFmYkV2MGQxams3R2JuWDcKKzRZVWx5SWZwcnpCVmRsbXoySkhZdjErMDRJekp0TDdjTDk3VUk3ZmswaTBPTVkwYWw4YStKUFFhNFVnNjExVApicUV0K25qQW1Ba2dlM0hYV0RCZEFYRDlNaGtDN1QvOW83N3pPUTFvbGk0Y1VkemxuWVdmem1XMFBkdU94dXZlCkFlWVk0d0lEQVFBQm80R2JNSUdZTUE0R0ExVWREd0VCL3dRRUF3SUhnREFNQmdOVkhSTUJBZjhFQWpBQU1CMEcKQTFVZERnUVdCQlNob05MK3Q3UnovcHNVYXEvTlBYTlBIKy9XbERBZkJnTlZIU01FR0RBV2dCVG5OQ291SXQ0NQpZR3UwbE01M2cyRXZNYUI4TlRBNEJnTlZIUjhFTVRBdk1DMmdLNkFwaGlkb2RIUndPaTh2ZDNkM0xtRndjR3hsCkxtTnZiUzloY0hCc1pXTmhMMmx3YUc5dVpTNWpjbXd3RFFZSktvWklodmNOQVFFRkJRQURnZ0VCQUY5cW1yVU4KZEErRlJPWUdQN3BXY1lUQUsrcEx5T2Y5ek9hRTdhZVZJODg1VjhZL0JLSGhsd0FvK3pFa2lPVTNGYkVQQ1M5Vgp0UzE4WkJjd0QvK2Q1WlFUTUZrbmhjVUp3ZFBxcWpubTlMcVRmSC94NHB3OE9OSFJEenhIZHA5NmdPVjNBNCs4CmFia29BU2ZjWXF2SVJ5cFhuYnVyM2JSUmhUekFzNFZJTFM2alR5Rll5bVplU2V3dEJ1Ym1taWdvMWtDUWlaR2MKNzZjNWZlREF5SGIyYnpFcXR2eDNXcHJsanRTNDZRVDVDUjZZZWxpblpuaW8zMmpBelJZVHh0UzZyM0pzdlpEaQpKMDcrRUhjbWZHZHB4d2dPKzdidFcxcEZhcjBaakY5L2pZS0tuT1lOeXZDcndzemhhZmJTWXd6QUc1RUpvWEZCCjRkK3BpV0hVRGNQeHRjYz0KLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo=',
    'fairplay_key_data_base64' => 'LS0tLS1CRUdJTiBDT05UQUlORVItLS0tLQpBQUVBQVIvcWRpY3lUdWJtMmxKTndMV1ZaT0xQSnpTSWF1MGJuT1lPSE10alZxc242dTFuY0Urb0ZQNkQ3VjNWCmplekJxQWNhRVpxUGNOT09yK3hFM2NkL1I0K1Q4OHMwSitFa0pQNnRPZzQ5U215ZkZUMlg0UDdYZExTNndEalAKY3piRmRDU0hpTVZmREJhY1pUaWxPNGNsdHllS3JzZHpLTlI5L3J5VXQ4TnJkY0VJd2lHWTBjYjNpcExLUnhHUwpYSWFMMnpYMy9HeE14UW0yRzdzL0IvWDBkdWEwd084enB6ZXE1bHkwc1lPQjE5cUdwaytKQ0hSaUtyUC9neFRaClJjZC9tTjVaM25WUEY4Qld2VEQ5UElvYldDZENxc3dCZzBvK1VyNnExZHFsZEpPM0FSOEFWTzFLUEFrVC8wV1QKdkR0MFpBbDJod3JEclpXdHJSd3RDNUlXZi9DY2UwaDZ0UXB4bDM3akFBWkdqcWNFM3F5dG4rdmh1SVQ2WklTUQpyK2x0T1B0Mk5vK3plVFh2TVExalJWUXlyRzFCNzRMWEpGcU1nQytGZGgzMDYvamRoMEtkeEVoeHdHanR4VGpICk5YRkhhV2Y0Nm9UaGVmWTBDM3NSclh1cENRSjg1ODNiRWFuUG8yUk1FL1dkY0pDODJFeEZma3FGRjNPSkU5dy8KV2w3NkFUZlVGaUVYRUFpUHVOQXk4Zlhhazk0Y3FyREhXeS9YbTFRV0o3Rnd4eDYzM2RnUXBFVWExSjBMaTNYZwpqaWJmczZQdDdpUkUzK3ZhTWViVW1BajZWZnczUjBQL253SzhzNnhubDJ1MUZsdEdXTkQxRWdoRVNEM1ExRk5mCkxlVWpOL1gwVmE0TEFzU0tGZ2NPSlloRi9renRLUFFqd0ZVNVFtd1FSeUI3aVhHM3lDbmdFZml6d3hhVEtUQzUKRmZFbi8xa3JlYndtOGZ3bW04NjllL3ZhTk81K285MFFibG9weDNUbnFRUWwyalYyZjhoa3FlYTlpUWRoL0JlTwpLUjVmcjR0bW9PSGNuUS9tRVNVZEUwdUcrRjhteGRBNVlUTzRhaElzaEZZajlEZzFVQkQvNGZHdWxkaCszZU50CkJQUVVveG5jTWd5VnFMMFRjaE90TXFOc3NnYkZXemUwRHBiMWU3OVVHUlJqdXN0QmlFTG9vY2s4amxtRWdwclgKZ3dLSmU5dkVqMDQ3Y2FUS2NSci9zKzN3b1ZkUWNQNDdZVEw0aVZKZ01jRHlZRFNGYk5lc3JXdlZ1KzhPZlJ0SwpUSEM0T2xQTmZWRTNXNXQyRWYwL0JlVERnL0FiUzUrSWNhSDdpeUhVZWRHWmxkRHpCWnhRMzdRRUNaYUZpUnpiCksrZWNXbWNMOXk3QnRoNGtaV3hJOE9vSzc3akQrb1JmWlVIZHM5OXNWbnNGZVRuQUVyL0RzaXVwTnlTRzZSdEcKVXJpOWZnRUYzUjJEb0lWaTlxQjdIUmJnM1VFTnZORlVFSVQ4VTdkb1lFVFBJSEVCUlVUU3k0MnhvbnVKNmxCNgpuOEEzaVpBTkR3N2ZzZWJUVzF6bnZuYmJGcC81YUhzMFJVNmNRenBTRlRIanRKb1hSQ091Y2RBRDNmY3VhMWhYCk14WENYV0drWDJOZnA2OFQvV0J4K0tlTDB0NGRFOXZrVnV4aEhjTjFZYS95OWZ2eFZZQmpSSVBEQXNBSGFhUnMKY05oZUdpTFNCTWh0Ui9kblVUMnA1aHhDRWNobnRjSTI5K21mYlV2VXIydVNrV3I4dFJVV0I0YjFZdmlVbUJScQpuQUV4L29WRHJlTDcvMnUxY0FhaHRhYWdaanBRUzlBNmhBSHA4RWVJNkg5dnZxcUtHMXY0TW9qa3NnalNlWDBuCnRWcHl0Yjg4TFZxNHRRNmp6U21BcXNzbmRzNmgwZzZCUHpFSWxFdDlLWWZLeURhbXZyOXM0czRZaldDcEgxT2UKL2ZMbEhYUzRURUMwOXdUYnpjQWw4dmZqUFpMdmpnMURyalZsUWU5K1FINGgrMElECi0tLS0tRU5EIENPTlRBSU5FUi0tLS0tCg==',
];
