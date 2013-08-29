#!/usr/bin/env php
<?php

// Test Driver
//
//

function readtestdata($filename) {
    $state = '';
    $fd = open($filename);
    if ($line == '--TEST--' || $line == '--INPUT--' || $line == '--EXPECTED--') {
        $state = $line;
    } else if ($state != '') {
        $info[$state] += $line + "\n";
    }

    return array(
        trim($info['--TEST--']),
        trim($info['--INPUT--']),
        trim($info['--EXPECTED--'])
    );
}

function fileproviders($pattern) {
    $args = array();
    foreach (glob($pattern) as $a) {
        array_push($args, array($a));
    }
    return $args;
}

function runtest($testname, $flag, $sqli_flags) {

}

class LibinjectionTestTokens extends PHPUnit_Framework_TestCase
{
    /**
     * @dataProvider filesTokens
     */
    public function testTokens($a) {
        True;
    }
    public function filesTokens() {
        return fileproviders('../tests/test-tokens-*.txt');
    }

    /**
     * @dataProvider filesFolding
     */
    public function testFolding($a) {
        return True;
    }
    public function filesFolding() {
        return fileproviders('../tests/test-folding-*.txt');
    }

    /**
     * @dataProvider filesFingerprints
     */
    public function testFingerprints($a) {
        return True;
    }
    public function filesFingerprints() {
        return fileproviders('../tests/test-sqli-*.txt');
    }
}
