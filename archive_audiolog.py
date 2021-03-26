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
            archive_filename = os.path.join(audiolog_dir, "audiolog.tgz")
            archive_file = tarfile.open(archive_filename, mode="w|gz")
            wavfiles = glob.glob(os.path.join(audiolog_dir,"*.wav"))
            for wavfile in wavfiles:
                print(wavfile)
                archive_file.add(wavfile, arcname=os.path.basename(wavfile))
            print(os.path.join(audiolog_dir, "audiolog.db"))
            archive_file.add(os.path.join(audiolog_dir,"audiolog.db"), arcname="audiolog_temp.db")
            archive_file.close()
            response.append(
                '<a href="?archive=audiolog.tgz">Created archive at {}</a>'.format(
                    archive_filename
                )
            )
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
        
