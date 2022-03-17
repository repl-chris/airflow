/*!
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

/* global moment */

import React from 'react';
import {
  Flex,
  Text,
  Box,
  Button,
  Link,
  Divider,
} from '@chakra-ui/react';
import { MdPlayArrow, MdOutlineAccountTree } from 'react-icons/md';

import { SimpleStatus } from '../../../StatusBox';
import { formatDateTime, formatDuration } from '../../../../datetime_utils';
import MarkFailedRun from './MarkFailedRun';
import MarkSuccessRun from './MarkSuccessRun';
import QueueRun from './QueueRun';
import ClearRun from './ClearRun';

const DagRun = ({
  dagRun: {
    dagId,
    state,
    runId,
    duration,
    dataIntervalStart,
    dataIntervalEnd,
    startDate,
    endDate,
    runType,
    lastSchedulingDecision,
    executionDate,
  },
}) => {
  const localTZ = moment.defaultZone.name.toUpperCase();

  const params = new URLSearchParams({
    dag_id: dagId,
    run_id: runId,
  }).toString();
  const detailsLink = `/dagrun_details?${params}`;
  const graphParams = new URLSearchParams({
    execution_date: executionDate,
  }).toString();
  const graphLink = `/dags/${dagId}/graph?${graphParams}`;

  return (
    <Box fontSize="12px" py="4px">
      <Flex justifyContent="space-between" alignItems="center">
        <Button as={Link} variant="ghost" colorScheme="blue" href={detailsLink}>More Details</Button>
        <Button as={Link} variant="ghost" colorScheme="blue" href={graphLink} leftIcon={<MdOutlineAccountTree />}>
          Graph
        </Button>
        <MarkFailedRun dagId={dagId} runId={runId} />
        <MarkSuccessRun dagId={dagId} runId={runId} />
      </Flex>
      <Divider my={3} />
      <Flex justifyContent="space-between" alignItems="center">
        <Text fontWeight="bold" ml="10px">Re-run:</Text>
        <Flex>
          <ClearRun dagId={dagId} runId={runId} />
          <QueueRun dagId={dagId} runId={runId} />
        </Flex>
      </Flex>
      <Divider my={3} />
      <Flex alignItems="center">
        <Text as="strong">Status:</Text>
        <SimpleStatus state={state} mx={2} />
        {state || 'no status'}
      </Flex>
      <br />
      <Text whiteSpace="nowrap">
        Run Id:
        {' '}
        {runId}
      </Text>
      <Text>
        Run Type:
        {' '}
        {runType === 'manual' && <MdPlayArrow style={{ display: 'inline' }} />}
        {runType}
      </Text>
      <Text>
        Duration:
        {' '}
        {formatDuration(duration)}
      </Text>
      {lastSchedulingDecision && (
      <Text>
        Last Scheduling Decision:
        {' '}
        {formatDateTime(lastSchedulingDecision)}
      </Text>
      )}
      <br />
      <Text as="strong">Data Interval:</Text>
      <Text>
        Start:
        {' '}
        {formatDateTime(dataIntervalStart)}
      </Text>
      <Text>
        End:
        {' '}
        {formatDateTime(dataIntervalEnd)}
      </Text>
      <br />
      <Text as="strong">UTC</Text>
      <Text>
        Started:
        {' '}
        {formatDateTime(moment.utc(startDate))}
      </Text>
      <Text>
        Ended:
        {' '}
        {endDate && formatDateTime(moment.utc(endDate))}
      </Text>
      {localTZ !== 'UTC' && (
        <>
          <br />
          <Text as="strong">
            Local:
            {' '}
            {moment().format('Z')}
          </Text>
          <Text>
            Started:
            {' '}
            {formatDateTime(startDate)}
          </Text>
          <Text>
            Ended:
            {' '}
            {endDate && formatDateTime(endDate)}
          </Text>
        </>
      )}
    </Box>
  );
};

export default DagRun;