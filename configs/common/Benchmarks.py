# Copyright (c) 2006-2007 The Regents of The University of Michigan
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors: Ali Saidi

from __future__ import print_function
from __future__ import absolute_import

from .SysPaths import script, disk, binary
from os import environ as env
from m5.defines import buildEnv

disk_path = '/research/hzhuo2/gem5-tail/images/arm2018/disks/'

class SysConfig:
    def __init__(self, script=None, mem=None, disk=None, rootdev=None,
                 os_type='linux'):
        self.scriptname = script
        self.diskname = disk
        self.memsize = mem
        self.root = rootdev
        self.ostype = os_type

    def script(self):
        if self.scriptname:
            return script(self.scriptname)
        else:
            return ''

    def mem(self):
        if self.memsize:
            return self.memsize
        else:
            return '128MB'

    def disk(self):
        if self.diskname:
            return disk(disk_path+self.diskname)
        elif buildEnv['TARGET_ISA'] == 'alpha':
            return env.get('LINUX_IMAGE', disk('linux-latest.img'))
        elif buildEnv['TARGET_ISA'] == 'x86':
            return env.get('LINUX_IMAGE', disk('x86root.img'))
        elif buildEnv['TARGET_ISA'] == 'arm':
            #return env.get('LINUX_IMAGE', disk('linux-aarch32-ael.img'))
            return env.get('LINUX_IMAGE',
                disk('aarch64-ubuntu-trusty-headless.img'))
        elif buildEnv['TARGET_ISA'] == 'sparc':
            return env.get('LINUX_IMAGE', disk('disk.s10hw2'))
        else:
            print("Don't know what default disk image to use for %s ISA" %
                buildEnv['TARGET_ISA'])
            exit(1)

    def rootdev(self):
        if self.root:
            return self.root
        else:
            return '/dev/sda1'

    def os_type(self):
        return self.ostype


# sphinximg= '/research/hzhuo2/gem5-tail/images/arm2018/'+
#             'disks/aarch64-trusty-tail-sphinx.img'
# masstreeimg= '/research/hzhuo2/gem5-tail/images/arm2018/'+
#             'disks/aarch64-trusty-tail-masstree.img'

# Benchmarks are defined as a key in a dict which is a list of SysConfigs
# The first defined machine is the test system, the others are driving systems

Benchmarks = {
    'PovrayBench':  [SysConfig('povray-bench.rcS', '512MB', 'povray.img')],
    'PovrayAutumn': [SysConfig('povray-autumn.rcS', '512MB', 'povray.img')],

    'NetperfStream':    [SysConfig('netperf-stream-client.rcS'),
                         SysConfig('netperf-server.rcS')],
    'NetperfStreamUdp': [SysConfig('netperf-stream-udp-client.rcS'),
                         SysConfig('netperf-server.rcS')],
    'NetperfUdpLocal':  [SysConfig('netperf-stream-udp-local.rcS')],
    'NetperfStreamNT':  [SysConfig('netperf-stream-nt-client.rcS'),
                         SysConfig('netperf-server.rcS')],
    'NetperfMaerts':    [SysConfig('netperf-maerts-client.rcS'),
                         SysConfig('netperf-server.rcS')],
    'SurgeStandard':    [SysConfig('surge-server.rcS', '512MB'),
                         SysConfig('surge-client.rcS', '256MB')],
    'SurgeSpecweb':     [SysConfig('spec-surge-server.rcS', '512MB'),
                         SysConfig('spec-surge-client.rcS', '256MB')],
    'Nhfsstone':        [SysConfig('nfs-server-nhfsstone.rcS', '512MB'),
                         SysConfig('nfs-client-nhfsstone.rcS')],
    'Nfs':              [SysConfig('nfs-server.rcS', '900MB'),
                         SysConfig('nfs-client-dbench.rcS')],
    'NfsTcp':           [SysConfig('nfs-server.rcS', '900MB'),
                         SysConfig('nfs-client-tcp.rcS')],
    'IScsiInitiator':   [SysConfig('iscsi-client.rcS', '512MB'),
                         SysConfig('iscsi-server.rcS', '512MB')],
    'IScsiTarget':      [SysConfig('iscsi-server.rcS', '512MB'),
                         SysConfig('iscsi-client.rcS', '512MB')],
    'Validation':       [SysConfig('iscsi-server.rcS', '512MB'),
                         SysConfig('iscsi-client.rcS', '512MB')],
    'Ping':             [SysConfig('ping-server.rcS','512MB',
                                   'aarch64-ubuntu-trusty-headless.img'),
                         SysConfig('ping-client.rcS','512MB',
                                   'aarch64-ubuntu-trusty-headless.img')],

    'ValAccDelay':      [SysConfig('devtime.rcS', '512MB')],
    'ValAccDelay2':     [SysConfig('devtimewmr.rcS', '512MB')],
    'ValMemLat':        [SysConfig('micro_memlat.rcS', '512MB')],
    'ValMemLat2MB':     [SysConfig('micro_memlat2mb.rcS', '512MB')],
    'ValMemLat8MB':     [SysConfig('micro_memlat8mb.rcS', '512MB')],
    'ValMemLat':        [SysConfig('micro_memlat8.rcS', '512MB')],
    'ValTlbLat':        [SysConfig('micro_tlblat.rcS', '512MB')],
    'ValSysLat':        [SysConfig('micro_syscall.rcS', '512MB')],
    'ValCtxLat':        [SysConfig('micro_ctx.rcS', '512MB')],
    'ValStream':        [SysConfig('micro_stream.rcS', '512MB')],
    'ValStreamScale':   [SysConfig('micro_streamscale.rcS', '512MB')],
    'ValStreamCopy':    [SysConfig('micro_streamcopy.rcS', '512MB')],

    'MutexTest':        [SysConfig('mutex-test.rcS', '128MB')],
    'ArmAndroid-GB':    [SysConfig('null.rcS', '256MB',
                    'ARMv7a-Gingerbread-Android.SMP.mouse.nolock.clean.img',
                    None, 'android-gingerbread')],
    'bbench-gb':        [SysConfig('bbench-gb.rcS', '256MB',
                            'ARMv7a-Gingerbread-Android.SMP.mouse.nolock.img',
                            None, 'android-gingerbread')],
    'ArmAndroid-ICS':   [SysConfig('null.rcS', '256MB',
                            'ARMv7a-ICS-Android.SMP.nolock.clean.img',
                            None, 'android-ics')],
    'bbench-ics':       [SysConfig('bbench-ics.rcS', '256MB',
                            'ARMv7a-ICS-Android.SMP.nolock.img',
                            None, 'android-ics')],
    'basic-ls':         [SysConfig('ls.rcS', '256MB',
                        'aarch64-ubuntu-trusty-headless.img')],
    'tail-sphinx':      [SysConfig('tail-sphinx-server.rcS','2048MB',
                        'aarch64-trusty-tail-sphinx.img'),
                         SysConfig('tail-sphinx-client.rcS','2048MB',
                        'aarch64-trusty-tail-sphinx.img')],
    'tail-masstree':    [SysConfig('tail-masstree-server.rcS','2048MB',
                        'aarch64-trusty-tail-masstree.img'),
                         SysConfig('tail-masstree-client.rcS','2048MB',
                        'aarch64-trusty-tail-masstree.img')],
    'tail-test':        [SysConfig('tail-test.rcS','256MB',
                                   'aarch64-trusty-tail.img')],

    'tail-ping':        [SysConfig('ping-server.rcS','2048MB',
                                   'aarch64-trusty-tail.img'),
                         SysConfig('ping-client.rcS','2048MB',
                                   'aarch64-trusty-tail.img')],

    'tail-sphinx-0.2':  [SysConfig('sphinx-server-2-2.rcS','2048MB',
                                   'aarch64-trusty-tail-sphinx.img'),
                         SysConfig('sphinx-client-0.2.rcS','2048MB',
                                   'aarch64-trusty-tail-sphinx.img')],
    'tail-sphinx-0.4':  [SysConfig('sphinx-server-2-2.rcS','2048MB',
                                   'aarch64-trusty-tail-sphinx.img'),
                         SysConfig('sphinx-client-0.4.rcS','2048MB',
                                   'aarch64-trusty-tail-sphinx.img')],
    'tail-sphinx-0.6':  [SysConfig('sphinx-server-2-2.rcS','2048MB',
                                   'aarch64-trusty-tail-sphinx.img'),
                         SysConfig('sphinx-client-0.6.rcS','2048MB',
                                   'aarch64-trusty-tail-sphinx.img')],
    'tail-sphinx-0.8':  [SysConfig('sphinx-server-2-2.rcS','2048MB',
                                   'aarch64-trusty-tail-sphinx.img'),
                         SysConfig('sphinx-client-0.8.rcS','2048MB',
                                   'aarch64-trusty-tail-sphinx.img')],
    'tail-sphinx-1.0':  [SysConfig('sphinx-server-2-2.rcS','2048MB',
                                   'aarch64-trusty-tail-sphinx.img'),
                         SysConfig('sphinx-client-1.0.rcS','2048MB',
                                   'aarch64-trusty-tail-sphinx.img')],

    'tail-masstree-100':[SysConfig('masstree-server-100.rcS','2048MB',
                                    'aarch64-trusty-tail-masstree.img'),
                         SysConfig('masstree-client-100.rcS','2048MB',
                                   'aarch64-trusty-tail-masstree.img')],
    'tail-masstree-200':[SysConfig('masstree-server-200.rcS','2048MB',
                                    'aarch64-trusty-tail-masstree.img'),
                         SysConfig('masstree-client-200.rcS','2048MB',
                                   'aarch64-trusty-tail-masstree.img')],
    'tail-masstree-300':[SysConfig('masstree-server-300.rcS','2048MB',
                                    'aarch64-trusty-tail-masstree.img'),
                         SysConfig('masstree-client-300.rcS','2048MB',
                                   'aarch64-trusty-tail-masstree.img')],
    'tail-masstree-400':[SysConfig('masstree-server-400.rcS','2048MB',
                                    'aarch64-trusty-tail-masstree.img'),
                         SysConfig('masstree-client-400.rcS','2048MB',
                                   'aarch64-trusty-tail-masstree.img')],
    'tail-masstree-500':[SysConfig('masstree-server-500.rcS','2048MB',
                                    'aarch64-trusty-tail-masstree.img'),
                         SysConfig('masstree-client-500.rcS','2048MB',
                                   'aarch64-trusty-tail-masstree.img')],
    'tail-masstree-600':[SysConfig('masstree-server-600.rcS','2048MB',
                                    'aarch64-trusty-tail-masstree.img'),
                         SysConfig('masstree-client-600.rcS','2048MB',
                                   'aarch64-trusty-tail-masstree.img')],
    'tail-masstree-700':[SysConfig('masstree-server-700.rcS','2048MB',
                                    'aarch64-trusty-tail-masstree.img'),
                         SysConfig('masstree-client-700.rcS','2048MB',
                                   'aarch64-trusty-tail-masstree.img')],
    'tail-masstree-800':[SysConfig('masstree-server-800.rcS','2048MB',
                                    'aarch64-trusty-tail-masstree.img'),
                         SysConfig('masstree-client-800.rcS','2048MB',
                                   'aarch64-trusty-tail-masstree.img')],

    'tail-masstree-100-w2r3':[SysConfig('masstree-server-100-w2r3.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img'),
                              SysConfig('masstree-client-100.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img')],
    'tail-masstree-100-w3r2':[SysConfig('masstree-server-100-w3r2.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img'),
                              SysConfig('masstree-client-100.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img')],
    'tail-masstree-100-w4r2':[SysConfig('masstree-server-100-w4r2.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img'),
                              SysConfig('masstree-client-100.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img')],

    'tail-masstree-200-w2r3':[SysConfig('masstree-server-200-w2r3.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img'),
                              SysConfig('masstree-client-200.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img')],
    'tail-masstree-200-w3r2':[SysConfig('masstree-server-200-w3r2.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img'),
                              SysConfig('masstree-client-200.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img')],
    'tail-masstree-200-w4r2':[SysConfig('masstree-server-200-w4r2.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img'),
                              SysConfig('masstree-client-200.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img')],

    'tail-masstree-300-w2r3':[SysConfig('masstree-server-300-w2r3.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img'),
                              SysConfig('masstree-client-300.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img')],
    'tail-masstree-300-w3r2':[SysConfig('masstree-server-300-w3r2.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img'),
                              SysConfig('masstree-client-300.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img')],
    'tail-masstree-300-w4r2':[SysConfig('masstree-server-300-w4r2.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img'),
                              SysConfig('masstree-client-300.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img')],

    'tail-masstree-400-w2r3':[SysConfig('masstree-server-400-w2r3.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img'),
                              SysConfig('masstree-client-400.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img')],
    'tail-masstree-400-w3r2':[SysConfig('masstree-server-400-w3r2.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img'),
                              SysConfig('masstree-client-400.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img')],
    'tail-masstree-400-w4r2':[SysConfig('masstree-server-400-w4r2.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img'),
                              SysConfig('masstree-client-400.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img')],

    'tail-masstree-500-w2r3':[SysConfig('masstree-server-500-w2r3.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img'),
                              SysConfig('masstree-client-500.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img')],
    'tail-masstree-500-w3r2':[SysConfig('masstree-server-500-w3r2.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img'),
                              SysConfig('masstree-client-500.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img')],
    'tail-masstree-500-w4r2':[SysConfig('masstree-server-500-w4r2.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img'),
                              SysConfig('masstree-client-500.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img')],

    'tail-masstree-600-w2r3':[SysConfig('masstree-server-600-w2r3.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img'),
                              SysConfig('masstree-client-600.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img')],
    'tail-masstree-600-w3r2':[SysConfig('masstree-server-600-w3r2.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img'),
                              SysConfig('masstree-client-600.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img')],
    'tail-masstree-600-w4r2':[SysConfig('masstree-server-600-w4r2.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img'),
                              SysConfig('masstree-client-600.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img')],

    'tail-masstree-700-w2r3':[SysConfig('masstree-server-700-w2r3.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img'),
                              SysConfig('masstree-client-700.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img')],
    'tail-masstree-700-w3r2':[SysConfig('masstree-server-700-w3r2.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img'),
                              SysConfig('masstree-client-700.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img')],
    'tail-masstree-700-w4r2':[SysConfig('masstree-server-700-w4r2.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img'),
                              SysConfig('masstree-client-700.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img')],

    'tail-masstree-800-w2r3':[SysConfig('masstree-server-800-w2r3.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img'),
                              SysConfig('masstree-client-800.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img')],
    'tail-masstree-800-w3r2':[SysConfig('masstree-server-800-w3r2.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img'),
                              SysConfig('masstree-client-800.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img')],
    'tail-masstree-800-w4r2':[SysConfig('masstree-server-800-w4r2.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img'),
                              SysConfig('masstree-client-800.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img')],

    'tail-masstree-900-w2r3':[SysConfig('masstree-server-900-w2r3.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img'),
                              SysConfig('masstree-client-900.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img')],
    'tail-masstree-900-w3r2':[SysConfig('masstree-server-900-w3r2.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img'),
                              SysConfig('masstree-client-900.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img')],
    'tail-masstree-900-w4r2':[SysConfig('masstree-server-900-w4r2.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img'),
                              SysConfig('masstree-client-900.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img')],

    'tail-masstree-1000-w2r3':[SysConfig('masstree-server-1000-w2r3.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img'),
                              SysConfig('masstree-client-1000.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img')],
    'tail-masstree-1000-w3r2':[SysConfig('masstree-server-1000-w3r2.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img'),
                              SysConfig('masstree-client-1000.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img')],
    'tail-masstree-1000-w4r2':[SysConfig('masstree-server-1000-w4r2.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img'),
                              SysConfig('masstree-client-1000.rcS',
                                        '2048MB',
                                        'aarch64-trusty-tail-masstree.img')],

}

benchs = list(Benchmarks.keys())
benchs.sort()
DefinedBenchmarks = ", ".join(benchs)
