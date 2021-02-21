import glob
import os
import tarfile
from naomi import paths
from naomi import plugin


class ArchiveAudiologPlugin(plugin.STTTrainerPlugin):
    def HandleCommand(self, command, description):
        response = []
        try:
            audiolog_dir = paths.sub("audiolog")
            archive_filename = os.path.expanduser("~/audiolog.tgz")
            archive_file = tarfile.open(archive_filename, mode="w|gz")
            archive_file.add(os.path.join(audiolog_dir,"audiolog.db"), arcname="audiolog_temp.db")
            wavfiles = glob.glob(os.path.join(audiolog_dir,"*.wav"))
            for wavfile in wavfiles:
                print(wavfile)
                archive_file.add(wavfile, arcname=os.path.basename(wavfile))
            archive_file.close()
            response.append("Created archive at {}".format(archive_filename))
        except Exception as e:
            continue_next = False
            message = "Unknown"
            if hasattr(e, "message"):
                message = e.message
            self._logger.error(
                "Error: {}".format(
                    message
                ),
                exc_info=True
            )
            response.append('<span class="failure">{}</span>'.format(
                message
            ))
        return response, "", ""
        
