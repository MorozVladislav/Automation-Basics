#!/usr/bin/env python3
# -*- coding: ascii -*-
import logging

from utils.ssh_client import SSHClient

logger = logging.getLogger(__name__)


class LinuxSteps(SSHClient):

    def __init__(self,
                 host=None,
                 username=None,
                 password=None,
                 key=None,
                 passphrase=None,
                 add_system_known_hosts=False,
                 **kwargs):

        super().__init__(host, username, password, key, passphrase, **kwargs)
        if add_system_known_hosts:
            self.add_system_known_hosts()

    def step(self, signature, get_signature=False, **kwargs):
        if get_signature:
            return signature
        else:
            logger.info('Executing {}'.format(signature))
            return self.execute(signature, **kwargs)

    @staticmethod
    def signature_creator(command, options):
        signature = [command]
        for option in options:
            if option is None or not options[option]:
                continue
            else:
                signature.append(option)
        return ' '.join(signature)

    def cd(self,
           path,
           force_symbolic_links=False,
           disregard_symbolic_links=False,
           raise_error=False,
           **kwargs):
        options = {
            '-L': force_symbolic_links,
            '-P': disregard_symbolic_links,
            '-e': raise_error,
            path: True
        }
        return self.step(self.signature_creator('cd', options), **kwargs)

    def mkdir(self,
              path,
              mode=None,
              parents=False,
              verbose=False,
              set_selinux_context_security_default=False,
              context=None,
              show_help=False,
              version=False,
              **kwargs):
        options = {
            '--mode={}'.format(mode): mode,
            '-p': parents,
            '-v': verbose,
            '-Z': set_selinux_context_security_default,
            '--context={}'.format(context): context,
            '--help': show_help,
            '--version': version,
            path: True
        }
        return self.step(self.signature_creator('mkdir', options), **kwargs)

    def rm(self,
           path,
           force=True,
           prompt=False,
           prompt_for_more_than_three=False,
           interactive=None,
           one_file_system=False,
           no_preserve_root=False,
           preserve_root=False,
           recursive=False,
           empty_directories=False,
           verbose=False,
           show_help=False,
           version=False,
           **kwargs):
        options = {
            '-f': force,
            '-i': prompt,
            '-I': prompt_for_more_than_three,
            'interactive={}'.format(interactive): interactive,
            'one-file-system': one_file_system,
            'no-preserve-root': no_preserve_root,
            'preserve-root': preserve_root,
            '-r': recursive,
            '-d': empty_directories,
            '-v': verbose,
            '--help': show_help,
            '--version': version,
            path: True
        }
        return self.step(self.signature_creator('rm', options), **kwargs)

    def ls(self,
           path='',
           show_all=False,
           almost_all=False,
           author=False,
           escape=False,
           block_size=None,
           ignore_backups=False,
           ctime=False,
           by_columns=False,
           color=None,
           directory=False,
           dired=False,
           do_not_sort=False,
           classify=False,
           file_type=False,
           formating=None,
           full_time=False,
           do_not_list_owner=False,
           group_directories_first=False,
           no_group=False,
           human_readable=False,
           human_readable_power_1000=False,
           dereference_command_line=False,
           dereference_command_line_symlink_to_dir=False,
           hide=None,
           indicator_style=None,
           inode=False,
           ignore=None,
           kinibytes=False,
           long_listing_format=False,
           dereference=False,
           fill_width_with_comma_separated_list=False,
           numeric_uid_gid=False,
           literal=False,
           do_not_list_group_information=False,
           indicator_style_slash=False,
           hide_control_chars=False,
           show_control_chars=False,
           quote_name=False,
           quoting_style=None,
           reverse=False,
           recursive=False,
           size=False,
           sort_by_file_size=False,
           sort=None,
           time=None,
           time_style=None,
           sort_by_modification_time=False,
           tabsize=None,
           access_time=False,
           list_in_directory_order=False,
           natural_sort_of_numbers=False,
           width=None,
           list_by_lines=False,
           sort_alphabetically=False,
           one_file_per_line=False,
           lcontext=False,
           context=False,
           scontext=False,
           show_help=False,
           version=False,
           **kwargs):
        options = {
            '-a': show_all,
            '-A': almost_all,
            '--author': author,
            '-b': escape,
            '--block-size={}'.format(block_size): block_size,
            '-B': ignore_backups,
            '-c': ctime,
            '-C': by_columns,
            '--color={}'.format(color): color,
            '-d': directory,
            '-D': dired,
            '-f': do_not_sort,
            '-F': classify,
            '--file-type': file_type,
            'format={}'.format(formating): formating,
            '--full-time': full_time,
            '-g': do_not_list_owner,
            'group-directories-first': group_directories_first,
            '-G': no_group,
            '-h': human_readable,
            '--si': human_readable_power_1000,
            '-H': dereference_command_line,
            'dereference-command-line-symlink-to-dir': dereference_command_line_symlink_to_dir,
            '--hide={}'.format(hide): hide,
            'indicator-style={}'.format(indicator_style): indicator_style,
            '-i': inode,
            '--ignore={}'.format(ignore): ignore,
            '-k': kinibytes,
            '-l': long_listing_format,
            '-L': dereference,
            '-m': fill_width_with_comma_separated_list,
            '-n': numeric_uid_gid,
            '-N': literal,
            '-o': do_not_list_group_information,
            '-p': indicator_style_slash,
            '-q': hide_control_chars,
            '--show-control-chars': show_control_chars,
            '-Q': quote_name,
            '--quoting-style={}'.format(quoting_style): quoting_style,
            '-r': reverse,
            '-R': recursive,
            '-s': size,
            '-S': sort_by_file_size,
            '--sort={}'.format(sort): sort,
            '--time={}'.format(time): time,
            '--time-styly={}'.format(time_style): time_style,
            '-t': sort_by_modification_time,
            '--tabsize={}'.format(tabsize): tabsize,
            '-u': access_time,
            '-U': list_in_directory_order,
            '-v': natural_sort_of_numbers,
            '--width={}'.format(width): width,
            '-x': list_by_lines,
            '-X': sort_alphabetically,
            '-1': one_file_per_line,
            '--lcontext': lcontext,
            '-Z': context,
            '--scontext': scontext,
            '--help': show_help,
            '--version': version,
            path: True
        }
        return self.step(self.signature_creator('ls', options), **kwargs)

    def cp(self,
           source,
           destination='',
           archive=False,
           attributes_only=False,
           backup=None,
           default_backup=False,
           copy_contents=False,
           no_dereference_preserve_links=False,
           force=False,
           interactive=False,
           follow_symbolic_links=False,
           link=False,
           dereference=False,
           no_clobber=False,
           no_dereference=False,
           preserve_mode_ownership_timestamps=False,
           preserve=None,
           no_preserve=None,
           parents=False,
           recursive=False,
           reflink=None,
           remove_destination=False,
           sparse=None,
           strip_trailing_slashes=False,
           symbolic_link=False,
           suffix=None,
           target_directory=None,
           no_target_directory=False,
           update=False,
           verbose=False,
           one_file_system=False,
           set_selinux_context_security_default=False,
           context=None,
           show_help=False,
           version=False,
           **kwargs):
        options = {
            '-a': archive,
            '--attributes-only': attributes_only,
            '--backup={}'.format(backup): backup,
            '-b': default_backup,
            '--copy-contents': copy_contents,
            '-d': no_dereference_preserve_links,
            '-f': force,
            '-i': interactive,
            '-H': follow_symbolic_links,
            '-l': link,
            '-L': dereference,
            '-n': no_clobber,
            '-P': no_dereference,
            '-p': preserve_mode_ownership_timestamps,
            '--preserve={}'.format(preserve): preserve,
            '--no-preserve={}'.format(no_preserve): no_preserve,
            '--parents': parents,
            '-r': recursive,
            '--reflink={}'.format(reflink): reflink,
            '--remove-destination': remove_destination,
            '--sparse={}'.format(sparse): sparse,
            '--strip-trailing-slashes': strip_trailing_slashes,
            '-s': symbolic_link,
            '--suffix={}'.format(suffix): suffix,
            '--target-directory={}'.format(target_directory): target_directory,
            '-T': no_target_directory,
            '-u': update,
            '-v': verbose,
            '-x': one_file_system,
            '-Z': set_selinux_context_security_default,
            '--context={}'.format(context): context,
            '--help': show_help,
            '--version': version,
            source: True,
            destination: True
        }
        return self.step(self.signature_creator('cp', options), **kwargs)

    def mv(self,
           source,
           directory='',
           backup=None,
           default_backup=False,
           force=False,
           interactive=False,
           no_clobber=False,
           strip_trailing_slashes=False,
           suffix=False,
           target_directory=None,
           no_target_directory=False,
           update=False,
           verbose=False,
           context=False,
           show_help=False,
           version=False,
           **kwargs):
        options = {
            '--backup={}'.format(backup): backup,
            '-b': default_backup,
            '-f': force,
            '-i': interactive,
            '-n': no_clobber,
            '--strip-trailing-slashes': strip_trailing_slashes,
            '--suffix={}'.format(suffix): suffix,
            '--target-directory={}'.format(target_directory): target_directory,
            '-T': no_target_directory,
            '-u': update,
            '-v': verbose,
            '-Z': context,
            '--help': show_help,
            '--version': version,
            source: True,
            directory: True
        }
        return self.step(self.signature_creator('mv', options), **kwargs)

    def date(self,
             date=None,
             file=None,
             iso_8601=None,
             reference=None,
             rfc_2822=False,
             rfc_3339=None,
             set_time=None,
             universal=False,
             show_help=False,
             version=False,
             date_format='',
             **kwargs):
        options = {
            '--date={}'.format(date): date,
            '--file={}'.format(file): file,
            '--iso-8601={}'.format(iso_8601): iso_8601,
            '--reference={}'.format(reference): reference,
            '--rfc-2822': rfc_2822,
            '--rgc-3339={}'.format(rfc_3339): rfc_3339,
            '--set={}'.format(set_time): set_time,
            '-u': universal,
            '--help': show_help,
            '--version': version,
            '+"{}"'.format(date_format): True
        }
        return self.step(self.signature_creator('date', options), **kwargs)
