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

function runtest($testname, $flag, $sqli_flags) {

}

function test_tokens() {

}

function test_tokens_mysql() {

}

function test_folding() {

}

function test_fingerprints() {

}
