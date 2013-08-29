<?php

// Test Driver
//
//

function readtestdata($filename) {
    $state = '';
    $info = array();

    $fd = fopen($filename, 'r');
    while (! feof($fd)) {
       $line = trim(fgets($fd));
       if ($line == '--TEST--' || $line == '--INPUT--' || $line == '--EXPECTED--') {
           $state = $line;
           $info[$state] = '';
       } else if ($state != '') {
           $info[$state] .= $line . "\n";
       }
    }
    fclose($fd);

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


class LibinjectionTestTokens extends PHPUnit_Framework_TestCase
{
    /**
     * @dataProvider filesTokens
     */
    public function testTokens($testfile) {
        return $this->_run($testfile, 'tokens', FLAG_QUOTE_NONE | FLAG_SQL_ANSI);
    }
    public function filesTokens() {
        return fileproviders('../tests/test-tokens-*.txt');
    }

    /**
     * @dataProvider filesFolding
     */
    public function testFolding($testfile) {
         return $this->_run($testfile, 'folding', FLAG_QUOTE_NONE | FLAG_SQL_ANSI);
    }
    public function filesFolding() {
        return fileproviders('../tests/test-folding-*.txt');
    }

    /**
     * @dataProvider filesFingerprints
     */
    public function testFingerprints($testfile) {
        return $this->_run($testfile, 'fingerprints', 0);
    }
    public function filesFingerprints() {
        return fileproviders('../tests/test-sqli-*.txt');
    }

    public function _run($testname, $flag, $sqli_flags) {
        $data =  readtestdata($testname);
        $sqlistate = new_libinjection_sqli_state();
        libinjection_sqli_init($sqlistate, $data[1], $sqli_flags);
        $actual = '';
        if ($flag == 'tokens') {
            while (libinjection_sqli_tokenize($sqlistate)) {
                $actual .= $this->print_token(libinjection_sqli_state_current_get($sqlistate)) . "\n";
            }
        } else if ($flag == 'folding') {
            $fingerprint = libinjection_sqli_fingerprint($sqlistate, $sqli_flags);
            for ($i  = 0; $i < strlen($fingerprint); $i++) {
                $r = libinjection_sqli_state_tokenvec_geti($sqlistate, $i);
                $actual .= $this->print_token($r) . "\n";
            }
        } else if ($flag == 'fingerprints') {
            $ok = libinjection_is_sqli($sqlistate);
            if ($ok == 1) {
                $actual = libinjection_sqli_state_fingerprint_get($sqlistate);
            }
        } else {
           $this->assert(False);
        }
        $actual = trim($actual);
        $this->assertEquals($actual, $data[2]);
    }

    public function print_token($tok) {
        $tt = libinjection_sqli_token_type_get($tok);
        $out = '';
        $out .= $tt;
        $out .= ' ';
        if ($tt == 's') {
            $out .= $this->print_token_string($tok);
        } else if ($tt == 'v') {
            $vc = libinjection_sqli_token_count_get($tok);
            if ($vc == 1) {
                $out .= '@';
            } else if ($vc == 2) {
                $out .= '@@';
            }
            $out .= $this->print_token_string($tok);
        } else {
            $out .= libinjection_sqli_token_val_get($tok);
        }
        return trim($out);
    }

    public function print_token_string($tok) {
       $out = '';
       $quote = libinjection_sqli_token_str_open_get($tok);
       if ($quote != "\0") {
           $out .= $quote;
       }
       $out .= libinjection_sqli_token_val_get($tok);
       $quote = libinjection_sqli_token_str_close_get($tok);
       if ($quote != "\0") {
           $out .= $quote;
       }
       return $out;
    }
}
