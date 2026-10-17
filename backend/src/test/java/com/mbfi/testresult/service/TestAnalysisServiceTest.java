package com.mbfi.testresult.service;

import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.Mockito.mock;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.mbfi.global.exception.BusinessException;
import com.mbfi.testresult.repository.TestResultRepository;
import org.junit.jupiter.api.Test;

class TestAnalysisServiceTest {
    private final TestAnalysisService service = new TestAnalysisService(
            mock(TestResultRepository.class),
            new ObjectMapper(),
            24
    );

    @Test
    void rejectsMissingQuestion() {
        assertThrows(
                BusinessException.class,
                () -> service.analyze(new ObjectMapper().createArrayNode().add("invalid"))
        );
    }

    @Test
    void rejectsDuplicateQuestion() throws Exception {
        var answers = new ObjectMapper().createArrayNode();
        for (int i = 0; i < 5; i++) {
            String questionId;
            if (i == 4) {
                questionId = "q1";
            } else {
                questionId = "q" + (i + 1);
            }
            answers.addObject()
                    .put("questionId", questionId)
                    .put("choice", "A");
        }
        assertThrows(BusinessException.class, () -> service.analyze(answers));
    }
}
