<?php
foreach (glob(__DIR__ . '/requests/*.xml') as $filename) {
    try {
        $requestfile = file_get_contents($filename);
        $encodedrequest = new DOMDocument();
        $encodedrequest->loadXML($requestfile);
        $activationDecoded = base64_decode($encodedrequest->getElementsByTagName('data')->item(0)->nodeValue, true);

        if ($activationDecoded === false) {
            throw new RuntimeException('Invalid activation payload');
        }

        $decodedrequest = new DOMDocument();
        $decodedrequest->loadXML($activationDecoded);
        $nodes = $decodedrequest->getElementsByTagName('dict')->item(0)->getElementsByTagName('*');

        $productType = 'Unknown';
        $productVersion = 'Unknown';
        $serialNumber = 'Unknown';

        for ($i = 0; $i < $nodes->length - 1; $i += 2) {
            switch ($nodes->item($i)->nodeValue) {
                case 'ProductType': $productType = $nodes->item($i + 1)->nodeValue; break;
                case 'ProductVersion': $productVersion = $nodes->item($i + 1)->nodeValue; break;
                case 'SerialNumber': $serialNumber = $nodes->item($i + 1)->nodeValue; break;
            }
        }

        echo htmlspecialchars(basename($filename), ENT_QUOTES, 'UTF-8') . ' -><br/>';
        $newfilename = str_replace(',', '.', $productType) . '_ios' . $productVersion . '_' . $serialNumber . '.xml';
        echo '<b style="color: green">' . htmlspecialchars($newfilename, ENT_QUOTES, 'UTF-8') . '</b>';
        echo ' ...................................................................... <b>' .
            (rename($filename, __DIR__ . '/requests/' . $newfilename) ? 'OK' : 'ERROR') . '</b>';
    } catch (Exception $e) {
        echo 'Could not parse request file <b>' . htmlspecialchars(basename($filename), ENT_QUOTES, 'UTF-8') . '</b>';
    }
    echo '<br/>------------------------------------------------------------------------------<br/>';
}
?>
