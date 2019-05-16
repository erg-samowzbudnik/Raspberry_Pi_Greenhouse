### Monitor should be built in such a way that the whole setup is modular and scalable
    Therefore we need a standardised way of writing into log files so that more
    sensors could be added easily and also that if it's decided to be needed we
    could easily use database instead of files.
    Log files are separate for each group of sensors. Easier to use data that way
###         


# Monitor will, at first, use defined sensors. We'll usr 1-wire sensors and
# write assuming their use. In later versions we can expand range of options
# but for now lets keep it simple.
