rule magic_string
{
    meta:
        description = "Samples that contain our magic string"

    strings:
        $ms = "_$_MAGICSTR_$_"

    condition:
        $ms
}
