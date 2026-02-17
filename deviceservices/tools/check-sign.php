<?php
$privateKeyPath = __DIR__.'/../certs/signature_private.key';
$privateKey = file_get_contents($privateKeyPath);
$pkeyid = openssl_pkey_get_private($privateKey);

if ($pkeyid === false) {
    exit('Failed to load private key.');
}

$accountTokenBase64 = base64_encode(
    '{' . "\n\t" . '"ActivationRandomness" = "F34182B4-4FE1-47D2-96F3-5851EF00D28F";' .
    "\n\t" . '"UniqueDeviceID" = "463fc92a2d3462dec0e2c4f98d445abe46730d6a";' . "\n" . '}'
);

$signature = '';
$signOk = openssl_sign($accountTokenBase64, $signature, $pkeyid, OPENSSL_ALGO_SHA256);

$publicKeyDetails = openssl_pkey_get_details($pkeyid);
$publicKey = is_array($publicKeyDetails) && isset($publicKeyDetails['key']) ? $publicKeyDetails['key'] : '';
$verifyOk = $publicKey !== '' ? openssl_verify($accountTokenBase64, $signature, $publicKey, OPENSSL_ALGO_SHA256) === 1 : false;

if (function_exists('openssl_pkey_free')) {
    openssl_pkey_free($pkeyid);
} else {
    openssl_free_key($pkeyid);
}

echo 'Signature (SHA-256) is ' . (($signOk && $verifyOk) ? 'correct' : 'incorrect');
?>
